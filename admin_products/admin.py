from django.contrib import admin
from . import models

admin.site.register(models.Brand)
admin.site.register(models.Categories)
admin.site.register(models.Product)
admin.site.register(models.Product_Image)



from admin_variant.models import *

admin.site.register(Product_Variant)
admin.site.register(Colors)
