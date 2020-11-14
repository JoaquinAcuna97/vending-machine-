from django.urls import path
from machines import api
urlpatterns = [
 path('',  api.home, name='home'),
]