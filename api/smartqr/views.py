from django.conf import settings
from django.core.cache import cache
from django.db import IntegrityError, transaction
from django.db.models import Count, F, Q
from django.db.models.functions import TruncDate
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import SimpleRateThrottle
from rest_framework.views import APIView

from .auth import authorize_manage
from .models import SmartQRCode
from .serializers import (
    SmartQRCodeCreateSerializer,
    SmartQRCodeReadSerializer,
    SmartQRScanSerializer,
    SmartQRCodeUpdateSerializer,
)
from .utils import (
    check_manage_token,
    client_ip,
    generate_manage_token,
    generate_slug,
    hash_ip,
    hash_manage_token,
    short_link_url_for_slug,
)


class SmartQRCreateThrottle(SimpleRateThrottle):
    scope = 'smartqr_create'

    def get_cache_key(self, request, view):
        ident = hash_ip(client_ip(request), daily=False)
        return self.cache_format % {'scope': self.scope, 'ident': ident}


class SmartQRCodeListCreateView(APIView):
    throttle_classes = [SmartQRCreateThrottle]

    def post(self, request):
        serializer = SmartQRCodeCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payload = serializer.validated_data
        raw_manage_token = generate_manage_token()
        token_hash = hash_manage_token(raw_manage_token)

        code = None
        for _ in range(10):
            slug = generate_slug(length=6)
            try:
                with transaction.atomic():
                    code = SmartQRCode.objects.create(
                        slug=slug,
                        target_url=payload['target_url'],
                        label=payload.get('label', ''),
                        tool_source=payload['tool_source'],
                        owner_email=payload.get('owner_email'),
                        manage_token_hash=token_hash,
                        created_ip_hash=hash_ip(client_ip(request), daily=False),
                    )
                break
            except IntegrityError:
                continue

        if code is None:
            return Response({'detail': 'Could not generate unique slug.'}, status=500)

        manage_base = settings.SMARTQR_FRONTEND_MANAGE_URL
        short_url = short_link_url_for_slug(code.slug)
        manage_url = f'{manage_base}?slug={code.slug}&token={raw_manage_token}'

        return Response(
            {
                'slug': code.slug,
                'short_url': short_url,
                'manage_url': manage_url,
                'manage_token': raw_manage_token,
                'qr_png_url': f'{short_url}.png?size=512&logo=1',
            },
            status=status.HTTP_201_CREATED,
        )


class SmartQRCodeDetailView(APIView):
    def _get_code(self, slug):
        return get_object_or_404(SmartQRCode, slug=slug)

    def _require_authorized(self, request, code):
        if not authorize_manage(request, code):
            return Response({'detail': 'Unauthorized.'}, status=status.HTTP_401_UNAUTHORIZED)
        return None

    def get(self, request, slug):
        code = self._get_code(slug)
        unauthorized = self._require_authorized(request, code)
        if unauthorized:
            return unauthorized
        return Response(SmartQRCodeReadSerializer(code).data)

    def patch(self, request, slug):
        code = self._get_code(slug)
        unauthorized = self._require_authorized(request, code)
        if unauthorized:
            return unauthorized

        serializer = SmartQRCodeUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        for field, value in serializer.validated_data.items():
            setattr(code, field, value)
        code.save()
        cache.delete(f'smartqr:slug:{code.slug}')
        return Response(SmartQRCodeReadSerializer(code).data)

    def delete(self, request, slug):
        code = self._get_code(slug)
        unauthorized = self._require_authorized(request, code)
        if unauthorized:
            return unauthorized
        code.is_active = False
        code.save(update_fields=['is_active', 'updated_at'])
        cache.delete(f'smartqr:slug:{code.slug}')
        return Response(status=status.HTTP_204_NO_CONTENT)


class SmartQRCodeScansView(APIView):
    def get(self, request, slug):
        code = get_object_or_404(SmartQRCode, slug=slug)
        if not authorize_manage(request, code):
            return Response({'detail': 'Unauthorized.'}, status=status.HTTP_401_UNAUTHORIZED)

        page = max(int(request.query_params.get('page', 1)), 1)
        page_size = min(max(int(request.query_params.get('page_size', 25)), 1), 100)
        queryset = code.scans.order_by('-created_at')
        total = queryset.count()
        start = (page - 1) * page_size
        end = start + page_size
        results = queryset[start:end]

        next_url = None
        if end < total:
            next_url = request.build_absolute_uri(f'?page={page + 1}&page_size={page_size}')

        previous_url = None
        if page > 1:
            previous_url = request.build_absolute_uri(f'?page={page - 1}&page_size={page_size}')

        return Response(
            {
                'count': total,
                'next': next_url,
                'previous': previous_url,
                'results': SmartQRScanSerializer(results, many=True).data,
            }
        )


class SmartQRCodeStatsView(APIView):
    RANGE_TO_DAYS = {'7d': 7, '30d': 30, '90d': 90}

    def get(self, request, slug):
        code = get_object_or_404(SmartQRCode, slug=slug)
        if not authorize_manage(request, code):
            return Response({'detail': 'Unauthorized.'}, status=status.HTTP_401_UNAUTHORIZED)

        selected_range = request.query_params.get('range', '7d')
        scans = code.scans.all()
        if selected_range in self.RANGE_TO_DAYS:
            cutoff = timezone.now() - timedelta(days=self.RANGE_TO_DAYS[selected_range])
            scans = scans.filter(created_at__gte=cutoff)

        total_scans = scans.count()
        unique_count = scans.filter(is_bot=False).values('ip_hash').distinct().count()

        by_day = (
            scans.annotate(date=TruncDate('created_at'))
            .values('date')
            .annotate(
                scans=Count('id'),
                unique=Count('ip_hash', filter=Q(is_bot=False), distinct=True),
            )
            .order_by('date')
        )
        by_device = (
            scans.values('device_type')
            .annotate(key=F('device_type'), scans=Count('id'))
            .values('key', 'scans')
            .order_by('-scans')
        )
        by_os = (
            scans.values('os_family')
            .annotate(key=F('os_family'), scans=Count('id'))
            .values('key', 'scans')
            .order_by('-scans')
        )
        by_browser = (
            scans.values('browser_family')
            .annotate(key=F('browser_family'), scans=Count('id'))
            .values('key', 'scans')
            .order_by('-scans')
        )
        by_country = (
            scans.values('country')
            .annotate(key=F('country'), scans=Count('id'))
            .values('key', 'scans')
            .order_by('-scans')
        )
        by_referrer = (
            scans.values('referrer')
            .annotate(key=F('referrer'), scans=Count('id'))
            .values('key', 'scans')
            .order_by('-scans')
        )

        normalized_referrer = [
            {'key': row['key'] or 'direct', 'scans': row['scans']} for row in by_referrer
        ]

        return Response(
            {
                'totals': {'scans': total_scans, 'unique': unique_count},
                'by_day': [
                    {'date': row['date'].isoformat(), 'scans': row['scans'], 'unique': row['unique']}
                    for row in by_day
                ],
                'by_device': list(by_device),
                'by_os': list(by_os),
                'by_browser': list(by_browser),
                'by_country': list(by_country),
                'by_referrer': normalized_referrer,
            }
        )


class SmartQRCodeClaimView(APIView):
    def post(self, request, slug):
        code = get_object_or_404(SmartQRCode, slug=slug)
        token = request.headers.get('X-Manage-Token', '') or request.META.get('HTTP_X_MANAGE_TOKEN', '')
        if not token or not check_manage_token(token, code.manage_token_hash):
            return Response({'detail': 'Unauthorized.'}, status=status.HTTP_401_UNAUTHORIZED)

        owner_email = None
        if request.user and request.user.is_authenticated:
            code.owner_user = request.user
            owner_email = request.user.email or None
        else:
            owner_email = request.data.get('email')
            if not owner_email:
                return Response({'email': ['This field is required.']}, status=status.HTTP_400_BAD_REQUEST)

        if owner_email:
            code.owner_email = owner_email

        new_manage_token = generate_manage_token()
        code.manage_token_hash = hash_manage_token(new_manage_token)
        code.save(update_fields=['owner_user', 'owner_email', 'manage_token_hash', 'updated_at'])
        cache.delete(f'smartqr:slug:{code.slug}')
        response_payload = {'status': 'claimed', 'slug': code.slug}
        if not (request.user and request.user.is_authenticated):
            response_payload['manage_token'] = new_manage_token
        return Response(response_payload)
