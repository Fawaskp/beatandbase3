# Generated by Django 4.1.7 on 2023-02-28 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_products', '0009_product_color_product_product_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product_Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='products')),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='product_img',
            field=models.ImageField(upload_to='products'),
        ),
    ]