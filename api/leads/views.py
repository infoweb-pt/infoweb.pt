from django.utils import timezone
from datetime import timedelta, datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle

from .serializers import (
    LostCustomerLeadSerializer,
    PresenceScoreLeadSerializer,
    ToolContactLeadSerializer,
)
from .models import LostCustomerLead, PresenceScoreLead, ToolContactLead

DEDUP_WINDOW_MINUTES = 60


class LeadSubmitThrottle(AnonRateThrottle):
    scope = 'lead_submit'


class LostCustomerLeadView(APIView):
    """
    POST /leads/lost-customers/
    Body: { "email": "...", "weekly_loss": 0.0, "monthly_loss": 0.0 }
    """
    throttle_classes = [LeadSubmitThrottle]

    def post(self, request):
        serializer = LostCustomerLeadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        cutoff = timezone.now() - timedelta(minutes=DEDUP_WINDOW_MINUTES)
        if LostCustomerLead.objects.filter(email=email, created_at__gte=cutoff).exists():
            return Response({'status': 'ok'}, status=status.HTTP_200_OK)

        serializer.save()
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)


class PresenceScoreLeadView(APIView):
    """
    POST /leads/presence-score/
    Body: { "email": "...", "score": 0-100, "answers": ["yes","no",...] }
    """
    throttle_classes = [LeadSubmitThrottle]

    def post(self, request):
        serializer = PresenceScoreLeadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        cutoff = timezone.now() - timedelta(minutes=DEDUP_WINDOW_MINUTES)
        if PresenceScoreLead.objects.filter(email=email, created_at__gte=cutoff).exists():
            return Response({'status': 'ok'}, status=status.HTTP_200_OK)

        serializer.save()
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)


class ToolContactLeadView(APIView):
    """
    POST /leads/tool-contact/
    Body: { "email": "...", "source": "whatsapp_qr_generator" }
    """

    throttle_classes = [LeadSubmitThrottle]

    def post(self, request):
        serializer = ToolContactLeadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        source = serializer.validated_data['source']
        cutoff = timezone.now() - timedelta(minutes=DEDUP_WINDOW_MINUTES)
        if ToolContactLead.objects.filter(
            email=email, source=source, created_at__gte=cutoff
        ).exists():
            return Response({'status': 'ok'}, status=status.HTTP_200_OK)

        serializer.save()
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)


class NewLeadsView(APIView):
    """
    GET /leads/new/?since=<ISO8601>
    Returns all leads created since the given timestamp.
    Query param: since (ISO 8601, e.g. 2026-05-15T00:00:00Z)
    """

    def get(self, request):
        since_str = request.query_params.get('since')
        if not since_str:
            return Response(
                {'error': 'Missing required query param: since'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Parse ISO 8601 timestamp
            since = datetime.fromisoformat(since_str.replace('Z', '+00:00'))
        except ValueError:
            return Response(
                {'error': 'Invalid timestamp format. Use ISO 8601 (e.g. 2026-05-15T00:00:00Z)'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Fetch leads from all models
        lost_customers = LostCustomerLead.objects.filter(created_at__gte=since)
        presence_scores = PresenceScoreLead.objects.filter(created_at__gte=since)
        tool_contacts = ToolContactLead.objects.filter(created_at__gte=since)

        # Build response
        leads = []

        for lead in lost_customers:
            leads.append({
                'type': 'lost_customer',
                'email': lead.email,
                'weekly_loss': str(lead.weekly_loss),
                'monthly_loss': str(lead.monthly_loss),
                'created_at': lead.created_at.isoformat(),
            })

        for lead in presence_scores:
            leads.append({
                'type': 'presence_score',
                'email': lead.email,
                'score': lead.score,
                'answers': lead.answers,
                'created_at': lead.created_at.isoformat(),
            })

        for lead in tool_contacts:
            leads.append({
                'type': 'tool_contact',
                'email': lead.email,
                'source': lead.source,
                'created_at': lead.created_at.isoformat(),
            })

        # Sort by created_at descending
        leads.sort(key=lambda x: x['created_at'], reverse=True)

        return Response({
            'since': since.isoformat(),
            'count': len(leads),
            'leads': leads,
        }, status=status.HTTP_200_OK)
