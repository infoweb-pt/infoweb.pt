from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from smartqr.models import SmartQRCode, SmartQRScan
from smartqr.utils import hash_manage_token


class SmartQRStatsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.raw_token = 'manage-secret-token'
        self.code = SmartQRCode.objects.create(
            slug='Ax9k2P',
            target_url='https://example.com',
            tool_source='generic',
            manage_token_hash=hash_manage_token(self.raw_token),
            created_ip_hash='created-ip-hash',
        )

    def _scan(self, **kwargs):
        defaults = {
            'code': self.code,
            'ip_hash': 'ip1',
            'country': 'PT',
            'city': '',
            'user_agent_raw': 'Mozilla/5.0',
            'device_type': 'mobile',
            'os_family': 'iOS',
            'os_version': '17',
            'browser_family': 'Safari',
            'browser_version': '17',
            'is_bot': False,
            'referrer': '',
            'language': 'pt-PT',
            'utm_source': '',
            'utm_medium': '',
            'utm_campaign': '',
        }
        defaults.update(kwargs)
        scan = SmartQRScan.objects.create(**defaults)
        if 'created_at' in kwargs:
            SmartQRScan.objects.filter(pk=scan.pk).update(created_at=kwargs['created_at'])
            scan.refresh_from_db()
        return scan

    def test_stats_shape_and_unique_excludes_bots(self):
        now = timezone.now()
        self._scan(ip_hash='u1', created_at=now - timedelta(days=1), referrer='')
        self._scan(ip_hash='u2', created_at=now - timedelta(days=1), device_type='desktop')
        self._scan(ip_hash='u2', created_at=now - timedelta(days=1), is_bot=True, browser_family='Googlebot')
        self._scan(ip_hash='u3', created_at=now, country='ES', os_family='Android', browser_family='Chrome', referrer='https://instagram.com')

        response = self.client.get('/smartqr/codes/Ax9k2P/stats/?range=7d', HTTP_X_MANAGE_TOKEN=self.raw_token)
        self.assertEqual(response.status_code, 200)
        body = response.json()

        self.assertEqual(body['totals']['scans'], 4)
        self.assertEqual(body['totals']['unique'], 3)
        self.assertIn('by_day', body)
        self.assertIn('by_device', body)
        self.assertIn('by_os', body)
        self.assertIn('by_browser', body)
        self.assertIn('by_country', body)
        self.assertIn('by_referrer', body)
        self.assertGreaterEqual(len(body['by_day']), 1)

    def test_stats_range_filters_old_scans(self):
        now = timezone.now()
        self._scan(ip_hash='old', created_at=now - timedelta(days=50))
        self._scan(ip_hash='new', created_at=now - timedelta(days=2))

        response = self.client.get('/smartqr/codes/Ax9k2P/stats/?range=7d', HTTP_X_MANAGE_TOKEN=self.raw_token)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['totals']['scans'], 1)
