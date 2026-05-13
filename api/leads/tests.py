import os
from io import StringIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase


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
