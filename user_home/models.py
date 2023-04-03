from django.apps import apps
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
import random
from admin_products.models import Product



class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, username,phone, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        phone = self.normalize_email(phone)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name)
        username = GlobalUserModel.normalize_username(username)
        user = self.model(phone=phone, username = username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone,username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, phone ,email, password, **extra_fields)

    def create_superuser(self,email, password, username=None,phone=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone,username, email, password, **extra_fields)

def generate_product_id():
    """Generate a unique four-digit product ID."""
    while True:
        new_id = random.randint(1000, 9999)
        if not Product.objects.filter(identification=new_id).exists():
            return new_id

class CustomUser(AbstractUser):
    is_blocked = models.BooleanField(default=False)
    identification = models.IntegerField(unique=True,default=generate_product_id)
    user_image = models.ImageField(upload_to='users',blank=True,null=True)
    username = models.CharField(_('username'),max_length=50,null=True)
    email = models.EmailField(_('email address'), unique=True,max_length=250)
    phone = models.CharField(max_length=12,blank=True,null=True,unique=True)
    wallet = models.DecimalField(max_digits=8,decimal_places=2, default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.email)

class UserOTP(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    time_st=models.DateTimeField(auto_now=True)
    otp=models.IntegerField()


class Mobile_Otp(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    time_st=models.DateTimeField(auto_now=True)
    otp=models.IntegerField()

    