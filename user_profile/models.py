from django.db import models
from user_home.models import CustomUser
import random

class User_Address(models.Model):
    fullname = models.CharField(max_length=100,null=True)
    contact_number = models.CharField(max_length=12,null=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    house_name = models.CharField(max_length=100)
    landmark = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)


    def __str__(self):
        return self.house_name


def generate_order_id():
    """Generate a unique four-digit order ID."""
    while True:
        new_id = random.randint(1000, 9999)
        if not True:
            return new_id