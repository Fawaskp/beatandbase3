from django.db import models
import random

def generate_id():
    """Generate a unique four-digit Brand ID."""
    while True:
        new_id = random.randint(1000, 9999)
        if not Brand.objects.filter(brand_id=new_id).exists():
            return new_id

class Brand(models.Model):
    brand_id = models.PositiveIntegerField(default=generate_id, unique=True)
    brand_img = models.ImageField(upload_to='brand',null=True,blank=True)
    brand_name = models.CharField(unique=True,max_length=50)
    brand_description = models.TextField

    def __str__(self):
        return self.brand_name
