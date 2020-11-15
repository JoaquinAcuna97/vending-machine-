from django.http import HttpResponse
from machines.models import VendingMachine as Machine
import json


def add_one_coin():
    return Machine.objects.add_one_coin()


def delete_coins():
    return Machine.objects.delete_coins()


def home(request):
    if request.method == 'GET':
        return HttpResponse('<html><title>Vending Machine</title></html>')

    if request.method == 'PUT':
        machine = add_one_coin()
        response = HttpResponse(status=204,
                                content_type='application/json'
                                )
        response['X-Coins'] = machine.coins
        return response

    if request.method == 'DELETE':
        coins_returned = delete_coins()
        response = HttpResponse(status=204,
                                content_type='application/json'
                                )
        response['X-Coins'] = coins_returned
        return response


def inventory(request):
    if request.method == 'GET':
        item_dicts = {}
        machine = Machine.objects.first()
        if machine is not None:
            item_dicts = [
                {'id': item.id,
                 'name': item.name,
                 'quantity': item.quantity}
                for item in machine.beverageitem_set.all()
            ]
        response = HttpResponse(json.dumps(item_dicts),
                                status=200,
                                content_type='application/json'
                                )
        return response


def refill(request):
    if request.method == 'POST':
        from django.core.management import call_command
        call_command('loaddata', 'fixtures')
        response = HttpResponse(status=200,
                                content_type='application/json'
                                )
        return response
