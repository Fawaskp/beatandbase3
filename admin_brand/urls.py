from django.urls import path
from . import views

urlpatterns = [
    path('',views.admin_brand,name='admin_brand'),
    path('delete_brand/<int:brand_id>',views.delete_brand,name='delete_brand'),
    path('edit_brand/<int:brand_id>',views.edit_brand,name='edit_brand'),
    path('add_brand',views.add_brand,name='add_brand'),
    path('search-brands',views.search_brands,name='search-brands'),

]
