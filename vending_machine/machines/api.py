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


def general_inventory(request):
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
    response = HttpResponse(status=404)
    return response


def inventory(request, id=None):
    if request.method == 'GET' and id is not None:
        machine = Machine.objects.first()
        if machine is not None:
            item = machine.beverageitem_set.get(id=id)
            if item is not None:
                item_dicts = {
                     'name': item.name,
                     'quantity': item.quantity}
                response = HttpResponse(json.dumps(item_dicts),
                                        status=200,
                                        content_type='application/json'
                                        )
                return response

    if request.method == 'PUT' and id is not None:
        machine = Machine.objects.first()
        if machine is not None:
            if machine.beverageitem_set.filter(id=id).exists():
                item = machine.beverageitem_set.get(id=id)
                if item.quantity > 0 and item.price <= machine.coins:
                    Machine.objects.buy_item(item.pk)
                    response = HttpResponse(json.dumps({"quantity":1}),
                                            status=200,
                                            content_type='application/json'
                                            )
                    item = machine.beverageitem_set.get(id=id)
                    machine = Machine.objects.first()
                    response['X-Coins'] = machine.coins
                    response['X-Inventory-Remaining'] = item.quantity
                    return response
                if item.price > machine.coins:
                    response = HttpResponse(status=400)
                    response['X-Coins'] = machine.coins
                    return response
            response = HttpResponse(status=404)
            response['X-Coins'] = machine.coins
            return response
    response = HttpResponse(status=404)
    response['X-Coins'] = 0 #machine does not exist
    return response


def refill(request):
    if request.method == 'POST':
        from django.core.management import call_command
        call_command('loaddata', 'fixtures')
        response = HttpResponse(status=200,
                                content_type='application/json'
                                )
        return response
    response = HttpResponse(status=404)
    return response
