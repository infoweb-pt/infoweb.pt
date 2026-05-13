from rest_framework import serializers

from .constants import ALLOWED_TOOL_SOURCES
from .models import SmartQRCode, SmartQRScan
from .utils import validate_target_url


class SmartQRCodeCreateSerializer(serializers.Serializer):
    target_url = serializers.CharField(max_length=2048)
    label = serializers.CharField(max_length=120, required=False, allow_blank=True)
    tool_source = serializers.CharField(max_length=64)
    owner_email = serializers.EmailField(required=False, allow_null=True)

    def validate_target_url(self, value):
        return validate_target_url(value)

    def validate_tool_source(self, value):
        if value not in ALLOWED_TOOL_SOURCES:
            raise serializers.ValidationError('Invalid tool_source.')
        return value


class SmartQRCodeUpdateSerializer(serializers.Serializer):
    target_url = serializers.CharField(max_length=2048, required=False)
    label = serializers.CharField(max_length=120, required=False, allow_blank=True)
    is_active = serializers.BooleanField(required=False)

    def validate_target_url(self, value):
        return validate_target_url(value)


class SmartQRCodeReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmartQRCode
        fields = (
            'id',
            'slug',
            'target_url',
            'label',
            'tool_source',
            'owner_user',
            'owner_email',
            'is_active',
            'expires_at',
            'created_at',
            'updated_at',
        )


class SmartQRScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmartQRScan
        exclude = ('ip_hash',)
