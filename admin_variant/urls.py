from django.urls import path
from .views import *
from .coupon_view import *

urlpatterns = [
    path('',product_variants,name= 'product_variants'),
    path('add_color',add_color,name= 'add_color'),
    path('add_variant',add_variant,name= 'add_variant'),
    path('edit_variant/<int:variant_id>',edit_variant,name= 'edit_variant'),
    path('delete_variant',delete_variant,name= 'delete_variant'),
    path('upload_images',upload_images,name='upload_images'), 
    path('search-variants',search_variants,name='search-variants'),

]