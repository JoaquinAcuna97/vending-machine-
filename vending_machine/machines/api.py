from django.http import HttpResponse
from machines.models import MachineFactory


def add_one_coin():
    machine_factory = MachineFactory()
    return machine_factory.add_one_coin('BeverageVendingMachineManager')


def delete_coins():
    machine_factory = MachineFactory()
    coins_returned = machine_factory.delete_coins('BeverageVendingMachineManager')
    return coins_returned


def home_get(request):
    if request.method == 'GET':
        return HttpResponse('<html><title>Vending VendingMachine</title></html>')


def home_put(request):
    if request.method == 'PUT':
        machine = add_one_coin()
        response = HttpResponse(status=204,
                                content_type='application/json'
                                )
        response['X-Coins'] = machine.coins
        return response

    response = HttpResponse(status=404)
    return response


def home_delete(request):
    if request.method == 'DELETE':
        coins_returned = delete_coins()
        response = HttpResponse(status=204,
                                content_type='application/json'
                                )
        response['X-Coins'] = coins_returned
        return response

    response = HttpResponse(status=404)
    return response


def home(request):
    if request.method == 'GET':
        return home_get(request)

    if request.method == 'PUT':
        return home_put(request)

    if request.method == 'DELETE':
        return home_delete(request)

    response = HttpResponse(status=404)
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
