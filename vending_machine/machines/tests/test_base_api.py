from django.test import TestCase

class TestPUTBase(TestCase):

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


class TestDELETEBase(TestCase):

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

