from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index_page'),
    path('user_register',views.user_register,name='user_register'),
    path('user_login',views.user_login,name='user_login'),
    path('user_logout',views.user_logout,name='user_logout'),
    path('categories',views.categories  ,name='categories'),
    path('mobile_login',views.mobile_login  ,name='mobile_login'),
    path('forgot_password',views.forgot_password  ,name='forgot_password'),
    path('reset_password',views.reset_password  ,name='reset_password'),
]