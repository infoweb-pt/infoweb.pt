from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LostCustomerLeadSerializer, PresenceScoreLeadSerializer


class LostCustomerLeadView(APIView):
    """
    POST /leads/lost-customers/
    Body: { "email": "...", "weekly_loss": 0.0, "monthly_loss": 0.0 }
    """
    def post(self, request):
        serializer = LostCustomerLeadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PresenceScoreLeadView(APIView):
    """
    POST /leads/presence-score/
    Body: { "email": "...", "score": 0-100, "answers": ["yes","no",...] }
    """
    def post(self, request):
        serializer = PresenceScoreLeadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
