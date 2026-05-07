from django.utils import timezone
from datetime import timedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle

from .serializers import LostCustomerLeadSerializer, PresenceScoreLeadSerializer
from .models import LostCustomerLead, PresenceScoreLead

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
