from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase
from rest_framework.test import APIClient

from smartqr.models import SmartQRCode
from smartqr.utils import hash_manage_token


class SmartQRManageTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='owner', password='pass123')
        self.raw_token = 'manage-secret-token'
        self.code = SmartQRCode.objects.create(
            slug='Ax9k2P',
            target_url='https://example.com',
            label='Old label',
            tool_source='generic',
            manage_token_hash=hash_manage_token(self.raw_token),
            created_ip_hash='created-ip-hash',
        )

    def test_get_detail_requires_token_or_owner(self):
        unauthorized = self.client.get('/smartqr/codes/Ax9k2P/')
        self.assertEqual(unauthorized.status_code, 401)

        authorized = self.client.get('/smartqr/codes/Ax9k2P/', HTTP_X_MANAGE_TOKEN=self.raw_token)
        self.assertEqual(authorized.status_code, 200)
        self.assertEqual(authorized.json()['slug'], 'Ax9k2P')

    def test_patch_with_wrong_token_is_401(self):
        response = self.client.patch(
            '/smartqr/codes/Ax9k2P/',
            {'label': 'New label'},
            format='json',
            HTTP_X_MANAGE_TOKEN='wrong-token',
        )
        self.assertEqual(response.status_code, 401)

    def test_patch_with_valid_token_updates_fields_and_busts_cache(self):
        cache.set(
            'smartqr:slug:Ax9k2P',
            {'id': str(self.code.id), 'slug': 'Ax9k2P', 'target_url': 'https://stale.example.com', 'is_active': True, 'expires_at': None},
            60,
        )
        response = self.client.patch(
            '/smartqr/codes/Ax9k2P/',
            {
                'target_url': 'https://new.example.com',
                'label': 'Updated label',
                'is_active': False,
            },
            format='json',
            HTTP_X_MANAGE_TOKEN=self.raw_token,
        )
        self.assertEqual(response.status_code, 200)
        self.code.refresh_from_db()
        self.assertEqual(self.code.target_url, 'https://new.example.com')
        self.assertEqual(self.code.label, 'Updated label')
        self.assertFalse(self.code.is_active)
        self.assertIsNone(cache.get('smartqr:slug:Ax9k2P'))

    def test_owner_can_manage_without_token(self):
        self.code.owner_user = self.user
        self.code.save(update_fields=['owner_user'])
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            '/smartqr/codes/Ax9k2P/',
            {'label': 'Owner updated'},
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        self.code.refresh_from_db()
        self.assertEqual(self.code.label, 'Owner updated')

    def test_delete_soft_deletes(self):
        response = self.client.delete('/smartqr/codes/Ax9k2P/', HTTP_X_MANAGE_TOKEN=self.raw_token)
        self.assertEqual(response.status_code, 204)
        self.code.refresh_from_db()
        self.assertFalse(self.code.is_active)
