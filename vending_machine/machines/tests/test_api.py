import json
from django.test import TestCase


class VendingMachineAPITest(TestCase):
    base_url = '/api/lists/{}/'

    def test_get_returns_json_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')

    def test_post_add_one_coin(self):
        response = self.client.put('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response['X-Coins'], 1)