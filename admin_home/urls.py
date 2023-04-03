from django.urls import path
from . import views
from admin_variant import coupon_view

urlpatterns = [
    path('',views.admin_home,name='admin_home'),
    path('admin_logout',views.admin_logout,name='admin_logout'),
    path('admin_login',views.admin_login,name='admin_login'),
    path('admin_profile',views.admin_profile,name='admin_profile'),
    path('admin_sales',views.admin_sales,name='admin_sales'),
    
    path('admin_orders',views.admin_orders,name='admin_orders'),
    path('admin-review',views.admin_review,name='admin_review'),
    path('delete-review',views.review_delete,name='delete-review'),
    path('change_order_status',views.change_order_status,name='change-order-status'),

    path('admin_coupon',coupon_view.admin_coupon,name='admin_coupon'),
    path('add_coupon',coupon_view.add_coupon,name='add_coupon'),
    path('delete_coupon',coupon_view.delete_coupon,name='delete_coupon'),
    path('edit_coupon',coupon_view.edit_coupon,name='edit_coupon'),
]
