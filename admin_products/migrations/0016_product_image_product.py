# Generated by Django 4.1.7 on 2023-03-03 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_products', '0015_alter_product_product_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_image',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='admin_products.product'),
            preserve_default=False,
        ),
    ]