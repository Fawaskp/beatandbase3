from django.db import models
from admin_products.models import Product
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import datetime
from datetime import date
from django.utils.translation import gettext_lazy as _

class Colors(models.Model):
    color_name = models.CharField(max_length=100)

    def __str__(self):
        return self.color_name
    
    
class Product_Variant(models.Model):
    thumbnail = models.ImageField(upload_to='variant_thumbnail',null=True,blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    color = models.ForeignKey(Colors, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(blank=True)
    price = models.PositiveIntegerField(null=True)
    is_available = models.BooleanField(default=True,blank=True)

    def __str__(self) -> str:
        return str(self.product) + ' with ' + str(self.color) +  ' color'
    

class Variant_images(models.Model):
    variant = models.ForeignKey(Product_Variant,on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to='variant_images')

    def __str__(self) -> str:
        return 'image of ' + str(self.variant)

global current_date;
current_date = datetime.utcnow()

def validate_expiry_date(value):
    min_date = date.today()
    if value < min_date:
        raise ValidationError(
            _(f"Expiry date cannot be earlier than {min_date}.")
        )

class Coupon(models.Model):
    name = models.CharField(max_length=15)
    min_amount = models.PositiveBigIntegerField()
    off_percent = models.PositiveIntegerField()
    max_discount = models.PositiveBigIntegerField()
    quantity = models.PositiveIntegerField()
    expiry_date = models.DateField(validators=[validate_expiry_date])
    status = models.BooleanField(default=True,null=True,blank=True)


    def __str__(self) -> str:
        return self.name