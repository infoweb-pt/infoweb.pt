from django.contrib.auth import get_user_model
from django.test import TestCase

from smartqr.models import SmartQRCode, SmartQRScan


class SmartQRAdminTests(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
        )
        self.client.force_login(self.admin)
        SmartQRCode.objects.create(
            slug='Ax9k2P',
            target_url='https://example.com',
            tool_source='generic',
            manage_token_hash='hash',
            created_ip_hash='created-ip-hash',
        )

    def test_smartqr_admin_changelists_load(self):
        code_list = self.client.get('/admin/smartqr/smartqrcode/')
        scan_list = self.client.get('/admin/smartqr/smartqrscan/')
        self.assertEqual(code_list.status_code, 200)
        self.assertEqual(scan_list.status_code, 200)

    def test_smartqr_change_page_loads_with_inline_scans(self):
        code = SmartQRCode.objects.get(slug='Ax9k2P')
        SmartQRScan.objects.create(
            code=code,
            ip_hash='ip-hash',
            country='PT',
            city='Porto',
            user_agent_raw='Mozilla/5.0',
            device_type='mobile',
            os_family='iOS',
            os_version='17',
            browser_family='Safari',
            browser_version='17',
            is_bot=False,
            referrer='',
            language='pt-PT',
        )
        response = self.client.get(f'/admin/smartqr/smartqrcode/{code.id}/change/')
        self.assertEqual(response.status_code, 200)
