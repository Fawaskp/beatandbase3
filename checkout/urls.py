from django.urls import path
from .views import *

urlpatterns = [
    path('',checkout,name='checkout'),
    path('cart',cart_checkout,name='cart_checkout'),
    path('add_address',add_address_checkout,name='add_address_checkout'),
]
