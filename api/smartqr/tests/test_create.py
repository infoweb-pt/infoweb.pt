from django.test import TestCase
from rest_framework.test import APIClient

from smartqr.models import SmartQRCode
from smartqr.utils import check_manage_token


class SmartQRCodeCreateEndpointTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_code_returns_slug_urls_and_manage_token(self):
        payload = {
            'target_url': 'https://wa.me/351912345678?text=Hi',
            'label': 'Front-window QR',
            'tool_source': 'whatsapp_qr',
            'owner_email': 'owner@cafe.pt',
        }
        response = self.client.post('/smartqr/codes/', payload, format='json')

        self.assertEqual(response.status_code, 201)
        body = response.json()
        self.assertIn('slug', body)
        self.assertIn('short_url', body)
        self.assertIn('manage_url', body)
        self.assertIn('manage_token', body)
        self.assertIn('qr_png_url', body)
        self.assertTrue(body['short_url'].endswith(f"/q/{body['slug']}"))

        code = SmartQRCode.objects.get(slug=body['slug'])
        self.assertNotEqual(body['manage_token'], code.manage_token_hash)
        self.assertTrue(check_manage_token(body['manage_token'], code.manage_token_hash))
        self.assertEqual(code.created_ip_hash, code.created_ip_hash)

    def test_create_rejects_invalid_scheme(self):
        response = self.client.post(
            '/smartqr/codes/',
            {'target_url': 'javascript:alert(1)', 'tool_source': 'whatsapp_qr'},
            format='json',
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('target_url', response.json())

    def test_create_rejects_unknown_tool_source(self):
        response = self.client.post(
            '/smartqr/codes/',
            {'target_url': 'https://example.com', 'tool_source': 'random_tool'},
            format='json',
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('tool_source', response.json())
