from django.http import HttpResponse
from machines.models import VendingMachine
import json
from machines.models import MachineFactory


def add_one_coin():
    machine_factory = MachineFactory()
    return machine_factory.add_one_coin('BeverageVendingMachineManager')


def delete_coins():
    machine_factory = MachineFactory()
    coins_returned = machine_factory.delete_coins('BeverageVendingMachineManager')
    return coins_returned


def home(request):
    if request.method == 'GET':
        return HttpResponse('<html><title>Vending VendingMachine</title></html>')

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
        machine = VendingMachine.load()
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


def inventory(request, item_id=None):
    machine = VendingMachine.load()
    if request.method == 'GET' and item_id is not None:
        if machine.beverageitem_set.filter(id=item_id).exists():
            item = machine.beverageitem_set.get(id=item_id)
            if item is not None:
                item_dicts = {
                     'name': item.name,
                     'quantity': item.quantity}
                response = HttpResponse(json.dumps(item_dicts),
                                        status=200,
                                        content_type='application/json'
                                        )
                return response

    if request.method == 'PUT' and item_id is not None:
        if machine.beverageitem_set.filter(id=item_id).exists():
            item = machine.beverageitem_set.get(id=item_id)
            if item.quantity > 0 and item.price <= machine.coins:
                machine_factory = MachineFactory()
                machine_factory.buy_item('BeverageVendingMachineManager', item_id=item.pk)
                response = HttpResponse(json.dumps({"quantity": 1}),
                                        status=200,
                                        content_type='application/json'
                                        )
                item.refresh_from_db()
                machine.refresh_from_db()
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
