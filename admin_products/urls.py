from django.urls import path
from . import views

urlpatterns = [
    path('',views.admin_products,name='admin_products'),
    path('delete/<int:product_id>',views.delete_product,name='delete_product'),
    path('edit/<int:product_id>',views.edit_product,name='edit_product'),
    path('add_product',views.add_product,name='add_product'),    
    path('search_product',views.search_product,name='search_product'),    
    # path('del_multiple_images',views.del_multiple_images,name='del_multiple_images'),    
]
