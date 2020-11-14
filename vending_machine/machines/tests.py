from django.urls import resolve
from django.test import TestCase
from machines.api import home
from machines.models import VendingMachine as Machine
import json


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home)

    def test_get_returns_json_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'text/html; charset=utf-8')


class MachineModelTest(TestCase):

    def test_saving_and_zero_coins_first(self):
        first_machine = Machine()
        first_machine.save()
        self.assertEqual(first_machine.coins, 0)

    def test_add_one_coin(self):
        first_machine = Machine.objects.add_one_coin()
        self.assertEqual(first_machine.coins, 1)

    def test_add_two_coins(self):
        Machine.objects.add_one_coin()
        first_machine = Machine.objects.add_one_coin()
        self.assertEqual(first_machine.coins, 2)

    def test_delete_zero_coin(self):
        first_machine = Machine.objects.create()
        coins_returned = Machine.objects.delete_coins()
        self.assertEqual(first_machine.coins, 0)
        self.assertEqual(coins_returned, 0)

    def test_delete_one_coin(self):
        Machine.objects.add_one_coin()
        coins_returned = Machine.objects.delete_coins()
        first_machine = Machine.objects.first()
        self.assertEqual(first_machine.coins, 0)
        self.assertEqual(coins_returned, 1)

    def test_delete_two_coins(self):
        Machine.objects.add_one_coin()
        Machine.objects.add_one_coin()
        coins_returned = Machine.objects.delete_coins()
        first_machine = Machine.objects.first()
        self.assertEqual(first_machine.coins, 0)
        self.assertEqual(coins_returned, 2)


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