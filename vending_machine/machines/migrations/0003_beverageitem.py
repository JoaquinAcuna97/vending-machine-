# Generated by Django 2.1.15 on 2020-11-15 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('machines', '0002_vendingmachine_coins'),
    ]

    operations = [
        migrations.CreateModel(
            name='BeverageItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('quantity', models.PositiveIntegerField(default=5)),
                ('price', models.PositiveIntegerField(default=2)),
                ('vending_machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='machines.VendingMachine')),
            ],
        ),
    ]
