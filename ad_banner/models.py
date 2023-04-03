from django.db import models
from admin_brand.models import Brand 

class Advertisement(models.Model):
    ad_image = models.ImageField(upload_to='advertisements')
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)