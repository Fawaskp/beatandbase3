from django.urls import path
from . import views

urlpatterns = [
    path('',views.ad_banner,name='ad_banner'),
    path('add_ad',views.add_ad,name='add_ad'),
    path('edit_ad/<int:ad_id>',views.edit_ad,name='edit_ad'),
    path('delete_ad/<int:ad_id>',views.delete_ad,name='delete_ad'),
]