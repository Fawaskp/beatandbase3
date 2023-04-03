from django.urls import path
from . import views

urlpatterns = [
    path('',views.user_profile  ,name='user_profile'),
    path('change_dp',views.change_dp  ,name='change_dp'),
    path('delete_address/<int:address_id>',views.delete_address  ,name='delete_address'),
    path('add_address',views.add_address  ,name='add_address'),
    path('edit_address/<int:address_id>',views.edit_address  ,name='edit_address'),
    path('edit_profile',views.edit_profile  ,name='edit_profile'),
    path('password_edit',views.password_edit  ,name='password_edit'),
]

