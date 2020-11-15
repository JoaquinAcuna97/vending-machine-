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
        first_item = Item()
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


class RelationItemMachine(TestCase):

    def test_add_item_to_a_machine(self):
        first_machine = Machine()
        first_machine.save()
        first_item = Item(name='Beer', vending_machine=first_machine)
        first_item.save()
        self.assertEqual(first_item.vending_machine.id, first_machine.id)

    def test_add_two_items_to_a_machine(self):
        first_machine = Machine()
        first_machine.save()
        first_item = Item(name='Beer', vending_machine=first_machine)
        first_item.save()
        second_item = Item(name='Hot chocolate', vending_machine=first_machine)
        second_item.save()
        self.assertEqual(first_machine.beverageitem_set.count(), 2)

    def test_add_three_items_to_a_machine(self):
        first_machine = Machine()
        first_machine.save()
        first_item = Item(name='Beer', vending_machine=first_machine)
        first_item.save()
        second_item = Item(name='Hot chocolate', vending_machine=first_machine)
        second_item.save()
        third_item = Item(name='Coffee', vending_machine=first_machine)
        third_item.save()
        self.assertEqual(first_machine.beverageitem_set.count(), 3)