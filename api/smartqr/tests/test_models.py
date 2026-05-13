from django.contrib.auth import get_user_model
from django.test import TestCase

from smartqr.models import SmartQRCode, SmartQRScan


class SmartQRCodeModelTests(TestCase):
    def test_fields_and_defaults(self):
        user = get_user_model().objects.create_user(username='owner', password='x')
        code = SmartQRCode.objects.create(
            slug='Ax9k2P',
            target_url='https://example.com',
            label='Front window',
            tool_source='whatsapp_qr',
            owner_user=user,
            owner_email='owner@example.com',
            manage_token_hash='hashed-token',
            created_ip_hash='created-ip-hash',
        )

        self.assertTrue(code.is_active)
        self.assertEqual(code.owner_user, user)
        self.assertEqual(code.owner_email, 'owner@example.com')
        self.assertEqual(code.slug, 'Ax9k2P')
        self.assertEqual(code.manage_token_hash, 'hashed-token')
        self.assertIsNotNone(code.created_at)
        self.assertIsNotNone(code.updated_at)

    def test_slug_is_unique(self):
        SmartQRCode.objects.create(
            slug='Ax9k2P',
            target_url='https://one.example.com',
            tool_source='generic',
            manage_token_hash='hash-1',
            created_ip_hash='ip-1',
        )
        with self.assertRaises(Exception):
            SmartQRCode.objects.create(
                slug='Ax9k2P',
                target_url='https://two.example.com',
                tool_source='generic',
                manage_token_hash='hash-2',
                created_ip_hash='ip-2',
            )


class SmartQRScanModelTests(TestCase):
    def test_scan_row_persists_analytics_fields(self):
        code = SmartQRCode.objects.create(
            slug='Ax9k2P',
            target_url='https://example.com',
            tool_source='generic',
            manage_token_hash='hashed-token',
            created_ip_hash='created-ip-hash',
        )

        scan = SmartQRScan.objects.create(
            code=code,
            ip_hash='ip-day-hash',
            country='PT',
            city='Porto',
            user_agent_raw='Mozilla/5.0',
            device_type='mobile',
            os_family='iOS',
            os_version='17.0',
            browser_family='Safari',
            browser_version='17.1',
            is_bot=False,
            referrer='https://instagram.com',
            language='pt-PT',
            utm_source='instagram',
            utm_medium='social',
            utm_campaign='menu_launch',
        )

        self.assertEqual(scan.code, code)
        self.assertEqual(scan.country, 'PT')
        self.assertEqual(scan.device_type, 'mobile')
        self.assertEqual(scan.browser_family, 'Safari')
        self.assertFalse(scan.is_bot)
        self.assertIsNotNone(scan.created_at)
