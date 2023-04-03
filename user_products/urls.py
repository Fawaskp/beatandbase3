from django.urls import path
from . import views
from . import reviews

urlpatterns = [
    path('',views.user_products,name='user_products'),
    path('product_detail/<int:product_id>',views.product_detail,name='product_detail'),
    path('variant_detail/<int:variant_id>',views.variant_detail,name='variant_detail'),
    path('search_product',views.search_product,name='user_search_product'),
    path('product-review/', reviews.submit_review, name="submit_review"),
]