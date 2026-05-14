import os
from io import StringIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from rest_framework.test import APIClient

from leads.models import ToolContactLead


class EnsureSuperuserCommandTests(TestCase):
    def test_creates_superuser_from_database_credentials_when_none_exists(self):
        with patch.dict(os.environ, {'DB_USER': 'infoweb_admin', 'DB_PASSWORD': 'secret-pass'}):
            call_command('ensure_superuser', stdout=StringIO())

        User = get_user_model()
        user = User.objects.get(username='infoweb_admin')

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password('secret-pass'))

    def test_keeps_existing_superuser(self):
        User = get_user_model()
        User.objects.create_superuser(username='existing', password='existing-pass')

        with patch.dict(os.environ, {'DB_USER': 'infoweb_admin', 'DB_PASSWORD': 'secret-pass'}):
            call_command('ensure_superuser', stdout=StringIO())

        self.assertEqual(User.objects.filter(is_superuser=True).count(), 1)
        self.assertFalse(User.objects.filter(username='infoweb_admin').exists())


class ToolContactLeadViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_post_creates_lead(self):
        url = '/leads/tool-contact/'
        payload = {'email': 'owner@example.com', 'source': 'whatsapp_qr_generator'}
        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok'})
        self.assertEqual(ToolContactLead.objects.count(), 1)
        lead = ToolContactLead.objects.first()
        self.assertEqual(lead.email, 'owner@example.com')
        self.assertEqual(lead.source, 'whatsapp_qr_generator')

    def test_duplicate_within_window_returns_ok_without_second_row(self):
        url = '/leads/tool-contact/'
        payload = {'email': 'dup@example.com', 'source': 'whatsapp_qr_generator'}
        self.client.post(url, payload, format='json')
        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ToolContactLead.objects.count(), 1)

    def test_post_accepts_wifi_qr_generator_source(self):
        url = '/leads/tool-contact/'
        payload = {'email': 'wifi@example.com', 'source': 'wifi_qr_generator'}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ToolContactLead.objects.filter(source='wifi_qr_generator').count(), 1)

