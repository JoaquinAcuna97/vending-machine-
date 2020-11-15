from django.core.exceptions import ValidationError
from django.test import TestCase
from machines.models import VendingMachine as Machine
from machines.models import BeverageItem as Item

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


class ItemModelTest(TestCase):

    def test_create_without_name(self):
        first_item = Item(price=2,
                          quantity=5)
        self.assertRaises(ValidationError, first_item.save())

    def test_create_item(self):
        first_item = Item(name='Beer')
        first_item.save()
        item_saved = Item.objects.get(id=first_item.id)
        self.assertEqual(item_saved.name, 'Beer')

    def test_create_item(self):
        first_item = Item(name='Beer',
                          price=2)
        first_item.save()
        item_saved = Item.objects.get(id=first_item.id)
        self.assertEqual(item_saved.name, 'Beer')
        self.assertEqual(item_saved.price, 2)

    def test_create_item(self):
        first_item = Item(name='Beer',
                          quantity=5)
        first_item.save()
        item_saved = Item.objects.get(id=first_item.id)
        self.assertEqual(item_saved.name, 'Beer')
        self.assertEqual(item_saved.quantity, 5)