from django.urls import resolve
from django.test import TestCase
from machines.views import home_page
from machines.models import VendingMachine as Machine


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)


class MachineModelTest(TestCase):

    def test_saving_and_zero_coins_first(self):
        first_machine = Machine()
        first_machine.save()
        self.assertEqual(first_machine.coins, 0)
