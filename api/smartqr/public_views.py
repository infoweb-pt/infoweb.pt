import logging
from io import BytesIO
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from django.core.cache import cache
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views import View
import qrcode
from qrcode.constants import ERROR_CORRECT_H, ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q

from .models import SmartQRCode, SmartQRScan
from .utils import client_ip, hash_ip, parse_user_agent, short_link_url_for_slug

logger = logging.getLogger(__name__)
SLUG_CACHE_TTL_SECONDS = 60
UTM_KEYS = {'utm_source', 'utm_medium', 'utm_campaign'}


class RedirectView(View):
    def _get_cached_code(self, slug):
        cache_key = f'smartqr:slug:{slug}'
        data = cache.get(cache_key)
        if data:
            return data

        code = get_object_or_404(SmartQRCode, slug=slug)
        data = {
            'id': code.id,
            'slug': code.slug,
            'target_url': code.target_url,
            'is_active': code.is_active,
            'expires_at': code.expires_at,
        }
        cache.set(cache_key, data, SLUG_CACHE_TTL_SECONDS)
        return data

    def _inactive_response(self):
        return HttpResponse('This QR is no longer active.', status=200)

    def _build_redirect_target_and_utm(self, target_url, incoming_query):
        incoming_params = parse_qsl(incoming_query, keep_blank_values=True)
        forwarded_incoming = []
        utm = {'utm_source': '', 'utm_medium': '', 'utm_campaign': ''}

        for key, value in incoming_params:
            if key in UTM_KEYS:
                utm[key] = value
            else:
                forwarded_incoming.append((key, value))

        parsed_target = urlparse(target_url)
        existing_target = parse_qsl(parsed_target.query, keep_blank_values=True)
        merged_query = urlencode(existing_target + forwarded_incoming, doseq=True)
        final_url = urlunparse(parsed_target._replace(query=merged_query))
        return final_url, utm

    def _build_scan_payload(self, request, code_id, utm):
        ua_raw = (request.META.get('HTTP_USER_AGENT', '') or '')[:512]
        parsed_ua = parse_user_agent(ua_raw)
        language = (request.META.get('HTTP_ACCEPT_LANGUAGE', '') or '').split(',')[0][:16]
        country = (request.META.get('HTTP_CF_IPCOUNTRY', '') or '').strip()[:2]
        referrer = (request.META.get('HTTP_REFERER', '') or '')[:512]

        return {
            'code_id': code_id,
            'ip_hash': hash_ip(client_ip(request), daily=True),
            'country': country,
            'city': '',
            'user_agent_raw': ua_raw,
            'device_type': parsed_ua['device_type'],
            'os_family': parsed_ua['os_family'][:32],
            'os_version': parsed_ua['os_version'][:32],
            'browser_family': parsed_ua['browser_family'][:32],
            'browser_version': parsed_ua['browser_version'][:32],
            'is_bot': parsed_ua['is_bot'],
            'referrer': referrer,
            'language': language,
            'utm_source': (utm['utm_source'] or '')[:64],
            'utm_medium': (utm['utm_medium'] or '')[:64],
            'utm_campaign': (utm['utm_campaign'] or '')[:64],
        }

    def get(self, request, slug):
        code = self._get_cached_code(slug)
        if not code['is_active']:
            return self._inactive_response()
        if code['expires_at'] and code['expires_at'] <= timezone.now():
            return self._inactive_response()

        redirect_url, utm = self._build_redirect_target_and_utm(
            code['target_url'],
            request.META.get('QUERY_STRING', ''),
        )
        scan_payload = self._build_scan_payload(request, code['id'], utm)

        def save_scan():
            try:
                SmartQRScan.objects.create(**scan_payload)
            except Exception:
                logger.exception('smartqr scan logging failed for slug=%s', slug)

        transaction.on_commit(save_scan)
        response = HttpResponseRedirect(redirect_url)
        response['Cache-Control'] = 'no-store'
        return response


class QRCodePngView(View):
    ERROR_CORRECTION = {
        'L': ERROR_CORRECT_L,
        'M': ERROR_CORRECT_M,
        'Q': ERROR_CORRECT_Q,
        'H': ERROR_CORRECT_H,
    }

    def get(self, request, slug):
        code = get_object_or_404(SmartQRCode, slug=slug)

        try:
            size = int(request.GET.get('size', '512'))
        except ValueError:
            size = 512
        size = max(128, min(1024, size))

        logo_enabled = request.GET.get('logo', '0') == '1'
        ec = request.GET.get('ec', 'M').upper()
        if ec not in self.ERROR_CORRECTION:
            ec = 'M'
        if logo_enabled:
            ec = 'H'

        qr = qrcode.QRCode(
            version=1,
            error_correction=self.ERROR_CORRECTION[ec],
            box_size=10,
            border=2,
        )
        qr.add_data(short_link_url_for_slug(code.slug))
        qr.make(fit=True)
        image = qr.make_image(fill_color='black', back_color='white').convert('RGB')
        image = image.resize((size, size))

        output = BytesIO()
        image.save(output, format='PNG')
        response = HttpResponse(output.getvalue(), content_type='image/png')
        response['Cache-Control'] = 'public, max-age=31536000, immutable'
        return response
