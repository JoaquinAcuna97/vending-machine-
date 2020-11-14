from django.http import HttpResponse
import json


def home(request):
    if request.method == 'PUT':

        response = HttpResponse(status=204,
                                content_type='application/json'
                                )
        response['X-Coins'] = 1
        return response

    elif request.method == 'GET':
        return HttpResponse(content_type='application/json')
