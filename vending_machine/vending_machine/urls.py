"""vending_machine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.urls import include
from machines import api
from machines import views
from machines import inventory_api
urlpatterns = [
    path('',  api.home, name='home'),
    path('refill', api.refill, name='refill'),
    path('inventory', inventory_api.general_inventory, name='general_inventory'),
    path('inventory/<int:item_id>', inventory_api.inventory, name='inventory'),
    path('admin/', admin.site.urls),
    path("update_server/", views.update, name="update"),
]
