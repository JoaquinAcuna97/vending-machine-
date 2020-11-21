from django.db import models
from abc import ABCMeta, abstractmethod


# Create your models here.

class MachineManager(models.Manager):
    class Meta:
        abstract = True

    @abstractmethod
    def add_one_coin(self):
        pass

    @abstractmethod
    def delete_coins(self):
        pass

    @abstractmethod
    def buy_item(self, item_id=None):
        pass


class BeverageVendingMachineManager(MachineManager):

    def add_one_coin(self):
        machine = VendingMachine.load()
        machine.coins += 1
        machine.save()
        return machine

    def delete_coins(self):
        machine = VendingMachine.load()
        coins_to_return = machine.coins
        machine.coins = 0
        machine.save()
        return coins_to_return

    def buy_item(self, item_id=None):
        machine = VendingMachine.load()
        if item_id is not None \
                and machine.beverageitem_set.filter(id=item_id).exists():
            item = machine.beverageitem_set.get(id=item_id)
            if machine.coins >= item.price and item.quantity > 0:
                item.quantity -= 1
                machine.coins -= item.price
                machine.save()
                item.save()
                return True
        return False


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Save object to the database. Removes all other entries if there
        are any.
        """
        self.__class__.objects.exclude(id=self.id).delete()
        super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        """
        Load object from the database. Failing that, create a new empty
        (default) instance of the object and return it (without saving it
        to the database).
        """

        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()


class VendingMachine(SingletonModel):
    coins = models.PositiveIntegerField(default=0)
    objects = BeverageVendingMachineManager()


class BeverageItem(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    quantity = models.PositiveIntegerField(default=5)
    price = models.PositiveIntegerField(default=2)
    vending_machine = models.ForeignKey(VendingMachine,
                                        on_delete=models.CASCADE,
                                        null=True)


class AnotherVendingMachineManager(MachineManager):

    def add_one_coin(self):
        pass

    def delete_coins(self):
        pass

    def buy_item(self, item_id=None):
        pass


## Machine factory defined
class MachineFactory(object):

    def add_one_coin(self, object_type):
        return eval(object_type)().add_one_coin()

    def delete_coins(self, object_type):
        return eval(object_type)().delete_coins()

    def buy_item(self, object_type, item_id=None):
        return eval(object_type)().buy_item(item_id)