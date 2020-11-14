from django.http import HttpResponse
from machines.models import VendingMachine as Machine
import json


def add_one_coin():
    return Machine.objects.add_one_coin()


def home(request):
    if request.method == 'PUT':
        machine = add_one_coin()
        response = HttpResponse(status=204,
                                content_type='application/json'
                                )
        response['X-Coins'] = machine.coins
        return response

    elif request.method == 'GET':
        return HttpResponse(content_type='application/json')


