# Generated by Django 4.1.7 on 2023-03-16 15:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('admin_variant', '0004_product_variant_thumbnail'),
        ('wishlist', '0004_wishlist_date_added'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='product',
        ),
        migrations.AddField(
            model_name='wishlist',
            name='variant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_variant.product_variant'),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
