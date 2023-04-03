from django.urls import path
from . import views

urlpatterns = [
    path('',views.admin_category,name='admin_category'),
    path('delete_category/<int:category_id>',views.delete_category,name='delete_category'),
    path('edit_category/<int:category_id>',views.edit_category,name='edit_category'),
    path('add_category',views.add_category,name='add_category'),
]
