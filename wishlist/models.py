from django.db import models
from admin_products.models import Product
from admin_variant.models import Product_Variant
from user_home.models import CustomUser

class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    variant = models.ForeignKey(Product_Variant,on_delete=models.CASCADE,null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.product) + ' by ' + str(self.user.username)