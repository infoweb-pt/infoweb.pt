from io import BytesIO
from unittest.mock import patch

from PIL import Image
from django.test import TestCase
from rest_framework.test import APIClient

from smartqr.models import SmartQRCode


class SmartQRPngTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.code = SmartQRCode.objects.create(
            slug='Ax9k2P',
            target_url='https://example.com',
            tool_source='generic',
            manage_token_hash='hash',
            created_ip_hash='created-ip-hash',
        )

    def test_png_endpoint_returns_image_with_immutable_cache(self):
        response = self.client.get('/q/Ax9k2P.png?size=512&ec=M')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/png')
        self.assertEqual(response['Cache-Control'], 'public, max-age=31536000, immutable')
        self.assertTrue(response.content.startswith(b'\x89PNG\r\n\x1a\n'))

    def test_png_size_is_clamped(self):
        low = self.client.get('/q/Ax9k2P.png?size=64')
        high = self.client.get('/q/Ax9k2P.png?size=2048')
        low_img = Image.open(BytesIO(low.content))
        high_img = Image.open(BytesIO(high.content))
        self.assertEqual(low_img.size, (128, 128))
        self.assertEqual(high_img.size, (1024, 1024))

    def test_png_encodes_absolute_redirect_url(self):
        with patch('smartqr.public_views.qrcode.QRCode.add_data') as add_data:
            response = self.client.get('/q/Ax9k2P.png?size=512&ec=M')
        self.assertEqual(response.status_code, 200)
        add_data.assert_called_once_with('https://infoweb.sousadev.com/q/Ax9k2P')
