from django.urls import path
from machines import api
urlpatterns = [
 path('',  api.home, name='home'),
 path('inventory', api.inventory, name='inventory'),
 path('refill', api.refill, name='refill'),
]