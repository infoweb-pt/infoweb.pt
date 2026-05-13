from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from smartqr.models import SmartQRCode
from smartqr.utils import hash_manage_token


class SmartQRClaimTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='claimer',
            email='claimer@example.com',
            password='pass123',
        )
        self.raw_token = 'manage-secret-token'
        self.code = SmartQRCode.objects.create(
            slug='Ax9k2P',
            target_url='https://example.com',
            tool_source='generic',
            manage_token_hash=hash_manage_token(self.raw_token),
            created_ip_hash='created-ip-hash',
        )

    def test_claim_assigns_owner_and_invalidates_token(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/smartqr/codes/Ax9k2P/claim/', {}, format='json', HTTP_X_MANAGE_TOKEN=self.raw_token)
        self.assertEqual(response.status_code, 200)
        self.code.refresh_from_db()
        self.assertEqual(self.code.owner_user_id, self.user.id)
        self.assertEqual(self.code.owner_email, 'claimer@example.com')

        reuse = self.client.post('/smartqr/codes/Ax9k2P/claim/', {}, format='json', HTTP_X_MANAGE_TOKEN=self.raw_token)
        self.assertEqual(reuse.status_code, 401)

    def test_email_only_claim_returns_new_token_for_further_management(self):
        response = self.client.post(
            '/smartqr/codes/Ax9k2P/claim/',
            {'email': 'owner@example.com'},
            format='json',
            HTTP_X_MANAGE_TOKEN=self.raw_token,
        )
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertIn('manage_token', body)

        self.code.refresh_from_db()
        self.assertIsNone(self.code.owner_user_id)
        self.assertEqual(self.code.owner_email, 'owner@example.com')

        manage = self.client.get('/smartqr/codes/Ax9k2P/', HTTP_X_MANAGE_TOKEN=body['manage_token'])
        self.assertEqual(manage.status_code, 200)
