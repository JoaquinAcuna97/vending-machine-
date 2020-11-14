from django.urls import resolve
from django.test import TestCase
from machines.api import home
from machines.models import VendingMachine as Machine
import json

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home)


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


class VendingMachineAPITest(TestCase):

    def test_get_returns_json_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')

    def test_put_204_and_json_content(self):
        response = self.client.put('/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response['content-type'], 'application/json')

    def test_put_one_coin(self):
        self.client.put('/')
        self.assertEqual(Machine.objects.count(), 1)
        new_machine = Machine.objects.first()
        self.assertEqual(new_machine.coins, 1)

    def test_put_twice(self):
        self.client.put('/')
        self.client.put('/')
        self.assertEqual(Machine.objects.count(), 1)
        new_machine = Machine.objects.first()
        self.assertEqual(new_machine.coins, 2)