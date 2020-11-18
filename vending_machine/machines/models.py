from django.db import models


# Create your models here.


class VendingMachineManager(models.Manager):

    def add_one_coin(self):
        machine = VendingMachine.objects.first()
        if machine is not None:
            machine.coins += 1
            machine.save()
        else:
            machine = VendingMachine.objects.create(coins=1)
        return machine

    def delete_coins(self):
        machine = VendingMachine.objects.first()
        coins_to_return = 0
        if machine is not None:
            coins_to_return = machine.coins
            machine.coins = 0
            machine.save()
        else:
            VendingMachine.objects.create()
        return coins_to_return

    def buy_item(self, item_id=None):
        machine = VendingMachine.objects.first()
        if machine is not None:
            if item_id is not None:
                item = machine.beverageitem_set.get(id=item_id)
                if machine.coins >= item.price and item.quantity > 0:
                    item.quantity -= 1
                    machine.coins -= item.price
                    machine.save()
                    item.save()
                    return True
        else:
            VendingMachine.objects.create()
        return False


class VendingMachine(models.Model):
    coins = models.PositiveIntegerField(default=0)
    objects = VendingMachineManager()


class BeverageItem(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    quantity = models.PositiveIntegerField(default=5)
    price = models.PositiveIntegerField(default=2)
    vending_machine = models.ForeignKey(VendingMachine,
                                        on_delete=models.CASCADE,null=True)
