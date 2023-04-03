from django.urls import path
from .views import *

urlpatterns = [
    path('',user_orders,name='user_orders'),
    path('place_order',place_order,name='place_order'),
    path('invoice/',order_invoice,name='invoice'),
    path('cancel_order/',cancel_order,name='cancel-order'),
    path('refund-order/',refund_order,name='refund-order')
]