import hmac
import secrets
from datetime import date
from hashlib import sha256
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from rest_framework import serializers
from user_agents import parse as parse_user_agent_string

BASE62_ALPHABET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
ALLOWED_SCHEMES = {'http', 'https', 'tel', 'mailto', 'whatsapp'}


def current_day_token():
    return date.today().isoformat()


def generate_slug(length=6):
    return ''.join(secrets.choice(BASE62_ALPHABET) for _ in range(length))


def generate_manage_token():
    return secrets.token_urlsafe(32)


def hash_manage_token(raw_token):
    return make_password(raw_token)


def check_manage_token(raw_token, token_hash):
    return check_password(raw_token, token_hash)


def _hmac_hex(secret, value):
    return hmac.new(secret.encode('utf-8'), value.encode('utf-8'), sha256).hexdigest()


def hash_ip(ip, daily=False):
    if daily:
        daily_seed = _hmac_hex(settings.SMARTQR_DAILY_SALT_SECRET, current_day_token())
        return _hmac_hex(daily_seed, ip or '')
    return _hmac_hex(settings.SMARTQR_IP_HASH_SECRET, ip or '')


def parse_user_agent(user_agent_raw):
    ua = parse_user_agent_string(user_agent_raw or '')

    if ua.is_mobile:
        device_type = 'mobile'
    elif ua.is_tablet:
        device_type = 'tablet'
    elif ua.is_pc:
        device_type = 'desktop'
    elif ua.is_bot:
        device_type = 'bot'
    else:
        device_type = 'other'

    browser_family = ua.browser.family or 'other'
    if browser_family == 'Mobile Safari':
        browser_family = 'Safari'

    return {
        'device_type': device_type,
        'os_family': ua.os.family or 'other',
        'os_version': ua.os.version_string or '',
        'browser_family': browser_family,
        'browser_version': ua.browser.version_string or '',
        'is_bot': ua.is_bot,
    }


def validate_target_url(url):
    parsed = urlparse(url or '')
    if len(url or '') > 2048:
        raise serializers.ValidationError('target_url is too long.')
    if parsed.scheme not in ALLOWED_SCHEMES:
        raise serializers.ValidationError('target_url scheme is not allowed.')
    return url


def client_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '') or ''
