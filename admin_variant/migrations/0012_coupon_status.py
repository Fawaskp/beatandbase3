# Generated by Django 4.1.7 on 2023-03-21 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_variant', '0011_alter_coupon_expiry_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='status',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]