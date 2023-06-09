# Generated by Django 4.1.7 on 2023-03-15 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_variant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Variant_images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='variant_images')),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_variant.product_variant')),
            ],
        ),
    ]
