from django.test import TestCase
from machines.models import VendingMachine as Machine
import json

class TestRefill(TestCase):

    def test_post_refill(self):
        response = self.client.post('/refill')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        first_machine = Machine.objects.first()
        self.assertEqual(first_machine.beverageitem_set.count(), 3)


class TestGETInventory(TestCase):

    def test_get_empty_inventory(self):
        response = self.client.get('/inventory')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            {}
        )

    def test_get_full_inventory(self):
        self.client.post('/refill')
        response = self.client.get('/inventory')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            [
                {
                    "id": 1,
                    "name": "Beer",
                    "quantity": 5
                },
                {
                    "id": 2,
                    "name": "Lemonade",
                    "quantity": 5
                },
                {
                    "id": 3,
                    "name": "Coffee",
                    "quantity": 5
                }
            ]
        )


class TestGETInventoryCertainItem(TestCase):

    def test_get_inventory_product_not_created(self):
        response = self.client.get('/inventory/2')
        self.assertEqual(response.status_code, 404)

    def test_get_inventory_product_not_created(self):
        self.client.post('/refill')
        response = self.client.get('/inventory/2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content.decode('utf8')),
            {
                "name": "Lemonade",
                "quantity": 5
            }
        )
