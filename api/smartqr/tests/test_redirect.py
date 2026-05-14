from datetime import timedelta

from django.core.cache import cache
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from smartqr.models import SmartQRCode, SmartQRScan


class SmartQRRedirectTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient()
        self.code = SmartQRCode.objects.create(
            slug='Ax9k2P',
            target_url='https://example.com/landing?foo=bar',
            tool_source='generic',
            manage_token_hash='hash',
            created_ip_hash='created-ip-hash',
        )

    def test_redirect_creates_scan_and_forwards_non_utm_query(self):
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.get(
                '/q/Ax9k2P?utm_source=ig&utm_medium=social&utm_campaign=spring&x=1',
                HTTP_USER_AGENT=(
                    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) '
                    'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1'
                ),
                HTTP_REFERER='https://instagram.com/some-post',
                HTTP_ACCEPT_LANGUAGE='pt-PT,pt;q=0.9',
                HTTP_CF_IPCOUNTRY='PT',
                REMOTE_ADDR='203.0.113.10',
            )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'https://example.com/landing?foo=bar&x=1')
        self.assertEqual(response['Cache-Control'], 'no-store')

        scan = SmartQRScan.objects.get(code=self.code)
        self.assertEqual(scan.utm_source, 'ig')
        self.assertEqual(scan.utm_medium, 'social')
        self.assertEqual(scan.utm_campaign, 'spring')
        self.assertEqual(scan.country, 'PT')
        self.assertEqual(scan.device_type, 'mobile')
        self.assertEqual(scan.os_family, 'iOS')
        self.assertEqual(scan.browser_family, 'Safari')
        self.assertFalse(scan.is_bot)
        self.assertEqual(scan.referrer, 'https://instagram.com/some-post')
        self.assertEqual(scan.language, 'pt-PT')

    def test_redirect_marks_bot_ua(self):
        with self.captureOnCommitCallbacks(execute=True):
            self.client.get(
                '/q/Ax9k2P',
                HTTP_USER_AGENT='Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
                REMOTE_ADDR='203.0.113.10',
            )
        scan = SmartQRScan.objects.get(code=self.code)
        self.assertTrue(scan.is_bot)

    def test_redirect_smartqr_q_prefix_matches_short_link(self):
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.get('/smartqr/q/Ax9k2P', REMOTE_ADDR='203.0.113.10')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'https://example.com/landing?foo=bar')

    def test_inactive_code_returns_200_and_no_scan(self):
        self.code.is_active = False
        self.code.save(update_fields=['is_active'])

        response = self.client.get('/q/Ax9k2P')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SmartQRScan.objects.filter(code=self.code).count(), 0)

    def test_expired_code_returns_200_and_no_scan(self):
        self.code.expires_at = timezone.now() - timedelta(minutes=1)
        self.code.save(update_fields=['expires_at'])

        response = self.client.get('/q/Ax9k2P')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SmartQRScan.objects.filter(code=self.code).count(), 0)
