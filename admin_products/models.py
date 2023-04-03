from django.db import models
from admin_brand.models import Brand
from admin_category.models import Categories
import random


def generate_product_id():
    """Generate a unique four-digit product ID."""
    while True:
        new_id = random.randint(1000, 9999)
        if not Product.objects.filter(identification=new_id).exists():
            return new_id

class Product(models.Model):
    identification = models.IntegerField(default=generate_product_id,null=True)
    product_name = models.CharField(unique=True,max_length=50)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)
    product_description = models.TextField(blank=True)

    def __str__(self):
        return self.product_name
    

class Product_Image(models.Model):
    product = models.ForeignKey(Product ,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products')
   
    def __str__(self) -> str:
        return str(self.product)
