from django.db import models

# Create your models here.


class VendingMachineManager(models.Manager):

    def add_one_coin(self):
        machine = VendingMachine.objects.first()
        if machine is not None:
            machine.coins +=1
            machine.save()
        else:
            machine = VendingMachine.objects.create(coins=1)
        return machine


class VendingMachine(models.Model):

    coins = models.PositiveIntegerField(default=0)
    objects = VendingMachineManager()


