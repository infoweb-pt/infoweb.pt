from unittest.mock import patch

from django.test import TestCase, override_settings
from rest_framework import serializers

from smartqr.utils import (
    check_manage_token,
    generate_manage_token,
    generate_slug,
    hash_ip,
    hash_manage_token,
    parse_user_agent,
    validate_target_url,
    short_link_url_for_slug,
)


class SmartQRUtilsTests(TestCase):
    def test_generate_slug_base62_length(self):
        slug = generate_slug()
        self.assertEqual(len(slug), 6)
        self.assertRegex(slug, r'^[A-Za-z0-9]{6}$')

    def test_manage_token_hash_roundtrip(self):
        token = generate_manage_token()
        token_hash = hash_manage_token(token)
        self.assertNotEqual(token, token_hash)
        self.assertTrue(check_manage_token(token, token_hash))
        self.assertFalse(check_manage_token('wrong-token', token_hash))

    def test_hash_ip_daily_rotates(self):
        with patch('smartqr.utils.current_day_token', return_value='2026-05-13'):
            first = hash_ip('203.0.113.10', daily=True)
            second = hash_ip('203.0.113.10', daily=True)
        self.assertEqual(first, second)

        with patch('smartqr.utils.current_day_token', return_value='2026-05-14'):
            rotated = hash_ip('203.0.113.10', daily=True)
        self.assertNotEqual(first, rotated)

    def test_parse_user_agent_iphone_safari(self):
        ua = (
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) '
            'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1'
        )
        parsed = parse_user_agent(ua)
        self.assertEqual(parsed['device_type'], 'mobile')
        self.assertEqual(parsed['os_family'], 'iOS')
        self.assertEqual(parsed['browser_family'], 'Safari')
        self.assertFalse(parsed['is_bot'])

    def test_parse_user_agent_bot(self):
        ua = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        parsed = parse_user_agent(ua)
        self.assertTrue(parsed['is_bot'])

    def test_short_link_url_for_slug_default_prefix(self):
        url = short_link_url_for_slug('Ab12cd')
        self.assertTrue(url.endswith('/smartqr/q/Ab12cd'))

    @override_settings(SMARTQR_PUBLIC_BASE_URL='https://api.example', SMARTQR_SHORT_LINK_PREFIX='q')
    def test_short_link_url_for_slug_custom_prefix(self):
        self.assertEqual(short_link_url_for_slug('Xy9'), 'https://api.example/q/Xy9')

    def test_validate_target_url_accepts_allowed_schemes(self):
        for url in [
            'https://example.com/path',
            'http://example.com',
            'tel:+351912345678',
            'mailto:owner@example.com',
            'whatsapp://send?phone=351912345678',
        ]:
            self.assertEqual(validate_target_url(url), url)

    def test_validate_target_url_rejects_disallowed_scheme(self):
        with self.assertRaises(serializers.ValidationError):
            validate_target_url('javascript:alert(1)')

        with self.assertRaises(serializers.ValidationError):
            validate_target_url('ftp://example.com')

    def test_validate_target_url_rejects_too_long(self):
        too_long = 'https://example.com/' + ('a' * 2050)
        with self.assertRaises(serializers.ValidationError):
            validate_target_url(too_long)
