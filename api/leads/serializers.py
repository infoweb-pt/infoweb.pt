from rest_framework import serializers
from .models import LostCustomerLead, PresenceScoreLead


class LostCustomerLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = LostCustomerLead
        fields = ['email', 'weekly_loss', 'monthly_loss']

    def validate_weekly_loss(self, value):
        if value < 0:
            raise serializers.ValidationError('weekly_loss must be a non-negative number.')
        return value

    def validate_monthly_loss(self, value):
        if value < 0:
            raise serializers.ValidationError('monthly_loss must be a non-negative number.')
        return value


class PresenceScoreLeadSerializer(serializers.ModelSerializer):
    score = serializers.IntegerField(min_value=0, max_value=100)
    answers = serializers.ListField(
        child=serializers.ChoiceField(choices=['yes', 'no']),
        min_length=1,
        max_length=20,
    )

    class Meta:
        model = PresenceScoreLead
        fields = ['email', 'score', 'answers']
