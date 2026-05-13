import uuid

from django.conf import settings
from django.db import models


class SmartQRCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.CharField(max_length=8, unique=True, db_index=True)
    target_url = models.URLField(max_length=2048)
    label = models.CharField(max_length=120, blank=True)
    tool_source = models.CharField(max_length=64)
    owner_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='smartqr_codes',
    )
    owner_email = models.EmailField(null=True, blank=True)
    manage_token_hash = models.CharField(max_length=128, unique=True)
    is_active = models.BooleanField(default=True)
    password_hash = models.CharField(max_length=128, null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_ip_hash = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['owner_user']),
            models.Index(fields=['tool_source']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f'{self.slug} ({self.tool_source})'


class SmartQRScan(models.Model):
    code = models.ForeignKey(
        SmartQRCode,
        on_delete=models.CASCADE,
        related_name='scans',
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    ip_hash = models.CharField(max_length=64)
    country = models.CharField(max_length=2, blank=True)
    city = models.CharField(max_length=120, blank=True)
    user_agent_raw = models.CharField(max_length=512)
    device_type = models.CharField(max_length=16, default='other')
    os_family = models.CharField(max_length=32, default='other')
    os_version = models.CharField(max_length=32, blank=True)
    browser_family = models.CharField(max_length=32, default='other')
    browser_version = models.CharField(max_length=32, blank=True)
    is_bot = models.BooleanField(default=False)
    referrer = models.CharField(max_length=512, blank=True)
    language = models.CharField(max_length=16, blank=True)
    utm_source = models.CharField(max_length=64, blank=True)
    utm_medium = models.CharField(max_length=64, blank=True)
    utm_campaign = models.CharField(max_length=64, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['code', 'created_at']),
            models.Index(fields=['country']),
            models.Index(fields=['device_type']),
        ]

    def __str__(self):
        return f'{self.code.slug} @ {self.created_at:%Y-%m-%d %H:%M:%S}'
