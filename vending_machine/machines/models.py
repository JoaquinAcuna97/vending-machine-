from django.db import models

# Create your models here.


class VendingMachine(models.Model):

    coins = models.PositiveIntegerField(default=0)