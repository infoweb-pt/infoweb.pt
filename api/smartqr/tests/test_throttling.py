from django.test import TestCase
from rest_framework.test import APIClient


class SmartQRCreateThrottleTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.payload = {
            'target_url': 'https://example.com',
            'tool_source': 'generic',
        }

    def test_create_is_throttled_by_ip_hash(self):
        responses = []
        for _ in range(11):
            responses.append(
                self.client.post(
                    '/smartqr/codes/',
                    self.payload,
                    format='json',
                    REMOTE_ADDR='203.0.113.10',
                )
            )

        self.assertEqual(responses[0].status_code, 201)
        self.assertEqual(responses[9].status_code, 201)
        self.assertEqual(responses[10].status_code, 429)
