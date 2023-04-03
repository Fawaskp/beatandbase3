from django.contrib import admin
from .models import Order,Order_item,Payment_methods

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'customer','placed_at', 'total', 'payment_method')

admin.site.register(Order,OrderAdmin)
admin.site.register(Order_item)
admin.site.register(Payment_methods)

