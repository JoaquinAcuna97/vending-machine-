from django.http import HttpResponse
from machines.models import VendingMachine
from machines.models import MachineFactory
import json

def general_inventory_get(request):
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


def general_inventory(request):
    if request.method == 'GET':
        return general_inventory_get(request)

    response = HttpResponse(status=404)
    return response


def inventory_get(request, item_id=None):
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

    response = HttpResponse(status=404)
    return response


def inventory_put(request, item_id=None):
    machine = VendingMachine.load()
    if request.method == 'PUT' and item_id is not None:
        if machine.beverageitem_set.filter(id=item_id).exists():
            item = machine.beverageitem_set.get(id=item_id)
            if item.price > machine.coins:
                response = HttpResponse(status=400)
                response['X-Coins'] = machine.coins
                return response

            elif item.quantity > 0:
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
        else:
            response = HttpResponse(status=404)
            response['X-Coins'] = machine.coins
            return response

    response = HttpResponse(status=404)
    return response


def inventory(request, item_id=None):
    if request.method == 'GET':
        return inventory_get(request, item_id)

    if request.method == 'PUT':
        return inventory_put(request, item_id)

    response = HttpResponse(status=404)
    return response