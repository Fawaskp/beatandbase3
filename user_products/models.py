from django.db import models
from user_home.models import CustomUser
from admin_products.models import Product

class ReviewRating(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField(blank=True, null=True)
    rating = models.FloatField()
    status = models.BooleanField(default=True)
    updated_at = models.DateField(auto_now=True)
    
    def str(self):
        return self.review