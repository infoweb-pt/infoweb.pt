from django.test import TestCase
from rest_framework.test import APIClient

from smartqr.models import SmartQRCode, SmartQRScan
from smartqr.utils import hash_manage_token


class SmartQRScansEndpointTests(TestCase):
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
        for idx in range(3):
            SmartQRScan.objects.create(
                code=self.code,
                ip_hash=f'ip-hash-{idx}',
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

    def test_scans_endpoint_is_paginated_and_hides_ip_hash(self):
        response = self.client.get(
            '/smartqr/codes/Ax9k2P/scans/?page=1&page_size=2',
            HTTP_X_MANAGE_TOKEN=self.raw_token,
        )
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body['count'], 3)
        self.assertEqual(len(body['results']), 2)
        self.assertIn('next', body)
        self.assertNotIn('ip_hash', body['results'][0])

    def test_scans_endpoint_requires_manage_auth(self):
        response = self.client.get('/smartqr/codes/Ax9k2P/scans/')
        self.assertEqual(response.status_code, 401)
