from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from machines.models import VendingMachine as Machine
from machines.models import BeverageItem as Item
from machines.models import MachineFactory


class MachineModelTest(TestCase):

    def test_saving_and_zero_coins_first(self):
        machine = Machine.load()
        machine.save()
        self.assertEqual(machine.coins, 0)

    def test_add_one_coin(self):
        machine_factory = MachineFactory()
        machine_factory.add_one_coin('BeverageVendingMachineManager')
        machine = Machine.load()
        self.assertEqual(machine.coins, 1)

    def test_add_two_coins(self):
        machine_factory = MachineFactory()
        machine_factory.add_one_coin('BeverageVendingMachineManager')
        machine_factory.add_one_coin('BeverageVendingMachineManager')
        machine = Machine.load()
        self.assertEqual(machine.coins, 2)

    def test_delete_zero_coin(self):
        machine_factory = MachineFactory()
        coins_returned = machine_factory.delete_coins('BeverageVendingMachineManager')
        machine = Machine.load()
        self.assertEqual(machine.coins, 0)
        self.assertEqual(coins_returned, 0)

    def test_delete_one_coin(self):
        machine_factory = MachineFactory()
        machine_factory.add_one_coin('BeverageVendingMachineManager')
        coins_returned = machine_factory.delete_coins('BeverageVendingMachineManager')
        machine = Machine.load()
        self.assertEqual(machine.coins, 0)
        self.assertEqual(coins_returned, 1)

    def test_delete_two_coins(self):
        machine_factory = MachineFactory()
        machine_factory.add_one_coin('BeverageVendingMachineManager')
        machine_factory.add_one_coin('BeverageVendingMachineManager')
        coins_returned = machine_factory.delete_coins('BeverageVendingMachineManager')
        machine = Machine.load()
        self.assertEqual(machine.coins, 0)
        self.assertEqual(coins_returned, 2)


class ItemModelTest(TestCase):

    def test_create_item(self):
        beer = Item(name='Beer')
        beer.save()
        item_saved = Item.objects.get(id=beer.id)
        self.assertEqual(item_saved.name, 'Beer')

    def test_create_item(self):
        beer = Item(name='Beer',
                          price=2)
        beer.save()
        item_saved = Item.objects.get(id=beer.id)
        self.assertEqual(item_saved.name, 'Beer')
        self.assertEqual(item_saved.price, 2)

    def test_create_item(self):
        beer = Item(name='Beer',
                          quantity=5)
        beer.save()
        item_saved = Item.objects.get(id=beer.id)
        self.assertEqual(item_saved.name, 'Beer')
        self.assertEqual(item_saved.quantity, 5)


class RelationItemMachine(TestCase):

    def test_add_item_to_a_machine(self):
        machine = Machine.load()
        machine.save()
        beer = Item(name='Beer', vending_machine=machine)
        beer.save()
        self.assertEqual(beer.vending_machine.id, machine.id)

    def test_add_two_items_to_a_machine(self):
        first_machine = Machine.load()
        first_machine.save()
        beer = Item(name='Beer', vending_machine=first_machine)
        beer.save()
        chocolate = Item(name='Hot chocolate', vending_machine=first_machine)
        chocolate.save()
        self.assertEqual(first_machine.beverageitem_set.count(), 2)

    def test_add_three_items_to_a_machine(self):
        machine = Machine.load()
        machine.save()
        beer = Item(name='Beer', vending_machine=machine)
        beer.save()
        chocolate = Item(name='Hot chocolate', vending_machine=machine)
        chocolate.save()
        coffee = Item(name='Coffee', vending_machine=machine)
        coffee.save()
        self.assertEqual(machine.beverageitem_set.count(), 3)


class BuyAItem(TestCase):

    def test_buy_one_item_success_no_remaining_coins(self):
        machine = Machine.load()
        machine.coins = 2
        machine.save()
        beer = Item(name='Beer', vending_machine=machine)
        beer.save()
        machine_factory = MachineFactory()
        machine_factory.buy_item('BeverageVendingMachineManager', item_id=beer.id)
        beer.refresh_from_db()
        machine = Machine.load()
        self.assertEqual(beer.quantity, 4)
        self.assertEqual(machine.coins, 0)

    def test_buy_one_item_success_one_remaining_coin(self):
        machine = Machine.load()
        machine.coins = 3
        machine.save()
        beer = Item(name='Beer', vending_machine=machine)
        beer.save()
        machine_factory = MachineFactory()
        machine_factory.buy_item('BeverageVendingMachineManager', item_id=beer.id)
        beer.refresh_from_db()
        machine = Machine.load()
        self.assertEqual(beer.quantity, 4)
        self.assertEqual(machine.coins, 1)

    def test_buy_two_times_one_item_success(self):
        machine = Machine.load()
        machine.coins = 4
        machine.save()
        beer = Item(name='Beer', vending_machine=machine)
        beer.save()
        machine_factory = MachineFactory()
        machine_factory.buy_item('BeverageVendingMachineManager', item_id=beer.id)
        machine_factory.buy_item('BeverageVendingMachineManager', item_id=beer.id)
        beer.refresh_from_db()
        machine = Machine.load()
        self.assertEqual(beer.quantity, 3)
        self.assertEqual(machine.coins, 0)

    def test_buy_two_different_items_success(self):
        machine = Machine.load()
        machine.coins = 4
        machine.save()
        beer = Item(name='Beer', vending_machine=machine)
        beer.save()
        lemonade = Item(name='Lemonade', vending_machine=machine)
        lemonade.save()
        machine_factory = MachineFactory()
        machine_factory.buy_item('BeverageVendingMachineManager', item_id=beer.id)
        machine_factory.buy_item('BeverageVendingMachineManager', item_id=lemonade.id)
        lemonade.refresh_from_db()
        machine = Machine.load()
        self.assertEqual(lemonade.quantity, 4)
        self.assertEqual(machine.coins, 0)


    def test_buy_item_no_stock(self):
        machine = Machine.load()
        machine.coins = 4
        machine.save()
        beer = Item(name='Beer', vending_machine=machine, quantity=0)
        beer.save()
        machine_factory = MachineFactory()
        machine_factory.buy_item('BeverageVendingMachineManager', item_id=beer.id)
        beer.refresh_from_db()
        machine = Machine.load()
        self.assertEqual(beer.quantity, 0)
        self.assertEqual(machine.coins, 4)

    def test_buy_item_insufficient_founds(self):
        machine = Machine.load()
        machine.coins = 4
        machine.save()
        beer = Item(name='Beer', vending_machine=machine, price=5)
        beer.save()
        machine_factory = MachineFactory()
        machine_factory.buy_item('BeverageVendingMachineManager', item_id=beer.id)
        beer.refresh_from_db()
        machine = Machine.load()
        self.assertEqual(beer.quantity, 5)
        self.assertEqual(machine.coins, 4)