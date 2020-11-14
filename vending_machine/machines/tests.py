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


class VendingMachineAPITest(TestCase):

    def test_get_returns_json_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')

    def test_post_add_one_coin(self):
        response = self.client.put('/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response['X-Coins'], '1')
