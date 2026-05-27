from rest_framework import serializers
from .models import (
    CompetitorVisibilityGapLead,
    LostCustomerLead,
    PresenceScoreLead,
    ToolContactLead,
    WebsiteHealthScorecardLead,
)
from .utils import is_disposable_email

TOOL_CONTACT_ALLOWED_SOURCES = frozenset(
    {'whatsapp_qr_generator', 'wifi_qr_generator'}
)


class LostCustomerLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = LostCustomerLead
        fields = ['email', 'weekly_loss', 'monthly_loss']

    def validate_email(self, value):
        if is_disposable_email(value):
            raise serializers.ValidationError(
                'Please use a real business or personal email address.'
            )
        return value.lower().strip()

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

    def validate_email(self, value):
        if is_disposable_email(value):
            raise serializers.ValidationError(
                'Please use a real business or personal email address.'
            )
        return value.lower().strip()


class ToolContactLeadSerializer(serializers.ModelSerializer):
    source = serializers.CharField(max_length=64)

    class Meta:
        model = ToolContactLead
        fields = ['email', 'source']

    def validate_email(self, value):
        if is_disposable_email(value):
            raise serializers.ValidationError(
                'Please use a real business or personal email address.'
            )
        return value.lower().strip()

    def validate_source(self, value):
        value = value.strip()
        if value not in TOOL_CONTACT_ALLOWED_SOURCES:
            raise serializers.ValidationError('Invalid source.')
        return value


class WebsiteHealthScorecardLeadSerializer(serializers.ModelSerializer):
    score = serializers.IntegerField(min_value=0, max_value=100)
    checks = serializers.JSONField()
    fixes = serializers.JSONField()

    class Meta:
        model = WebsiteHealthScorecardLead
        fields = ['email', 'url', 'score', 'checks', 'fixes']

    def validate_email(self, value):
        if is_disposable_email(value):
            raise serializers.ValidationError(
                'Please use a real business or personal email address.'
            )
        return value.lower().strip()

    def validate_url(self, value):
        value = value.strip()
        if not value or len(value) > 500:
            raise serializers.ValidationError('url must be between 1 and 500 characters.')
        return value

    def validate_checks(self, value):
        if not isinstance(value, list) or not value or len(value) > 10:
            raise serializers.ValidationError('checks must be a non-empty list (max 10 items).')
        return value

    def validate_fixes(self, value):
        if not isinstance(value, list) or len(value) > 20:
            raise serializers.ValidationError('fixes must be a list (max 20 items).')
        return value


class CompetitorVisibilityGapLeadSerializer(serializers.ModelSerializer):
    score = serializers.IntegerField(min_value=0, max_value=100)
    answers = serializers.ListField(
        child=serializers.ChoiceField(choices=['yes', 'no']),
        min_length=1,
        max_length=20,
    )

    class Meta:
        model = CompetitorVisibilityGapLead
        fields = ['email', 'score', 'answers']

    def validate_email(self, value):
        if is_disposable_email(value):
            raise serializers.ValidationError(
                'Please use a real business or personal email address.'
            )
        return value.lower().strip()
