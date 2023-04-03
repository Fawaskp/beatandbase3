from django.urls import path
from .views import *

urlpatterns = [
    path('',wishlist,name='wishlist'),
    path('add',add_wishlist,name='add-wishlist'),
    path('delete/<int:variant_id>',delete_wishlist,name='delete-wishlist')
]
