from django.db import models
from admin_variant.models import Product_Variant, Coupon
from user_home.models import CustomUser
import random



def generate_cart_id():
    """Generate a unique eight-digit cart ID."""
    while True:
        new_id = random.randint(10000000, 99999999)
        if not Cart.objects.filter(cart_id=new_id).exists():
            return new_id


class Cart(models.Model):
    cart_id = models.IntegerField(unique=True,default=generate_cart_id)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True,blank=True)    
    coupon_discount = models.BigIntegerField(null=True,blank=True)

    def __str__(self):
        return f"Cart ({self.id})"

    def total_item_price(self):
        total = 0
        cart_items = self.cartitem_set.all()  # Get all cart items for this cart
        for item in cart_items:
            total += item.variant.price * item.qty
        return total
    
    def total_qty(self):
        total_qty = 0
        cart_items = self.cartitem_set.all()  # Get all cart items for this cart
        for item in cart_items:
            total_qty += item.qty
        return total_qty


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    variant = models.ForeignKey(Product_Variant, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()
    

    def __str__(self):
        return f"{self.qty} x {self.variant.product.product_name} ({self.variant.color})"
    



