from django.urls import path
from . import views

urlpatterns = [
    path('',views.user_list,name='user_list'),
    path('user_action/<int:user_id>',views.user_action,name='user_action'),
    path('search-user',views.search_users,name='search-users'),
]