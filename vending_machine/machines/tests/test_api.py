from django.test import TestCase
import json


class VendingMachineAPITestPUT(TestCase):

    def test_put_204_and_json_content(self):
        response = self.client.put('/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response['content-type'], 'application/json')

    def test_put_one_coin(self):
        response = self.client.put('/')
        self.assertEqual(response['X-Coins'], '1')

    def test_put_twice(self):
        self.client.put('/')
        response = self.client.put('/')
        self.assertEqual(response['X-Coins'], '2')


class VendingMachineAPITestDELETE(TestCase):

    def test_delete_returns_json_204(self):
        response = self.client.delete('/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response['content-type'], 'application/json')

    def test_delete_without_coins(self):
        response = self.client.delete('/')
        self.assertEqual(response['X-Coins'], '0')

    def test_delete_one_coin(self):
        self.client.put('/')
        response = self.client.delete('/')
        self.assertEqual(response['X-Coins'], '1')

    def test_delete_two_coins(self):
        self.client.put('/')
        self.client.put('/')
        response = self.client.delete('/')
        self.assertEqual(response['X-Coins'], '2')

    def test_delete_three_coins(self):
        self.client.put('/')
        self.client.put('/')
        self.client.put('/')
        response = self.client.delete('/')
        self.assertEqual(response['X-Coins'], '3')


class VendingMachineAPITestGETInventory(TestCase):

    def test_get_empty_inventory(self):
        response = self.client.get('/inventory')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            {}
        )

    def test_get_full_inventory(self):
        self.client.get('/refill')
        response = self.client.get('/inventory')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            {[
                {
                    "pk": 1,
                    "fields": {
                        "name": "Beer",
                        "vending_machine": 1
                    }
                },
                {
                    "pk": 2,
                    "fields": {
                        "name": "Lemonade",
                        "vending_machine": 1
                    }
                },
                {
                    "pk": 3,
                    "fields": {
                        "name": "Coffee",
                        "vending_machine": 1
                    }
                }
            ]}
        )