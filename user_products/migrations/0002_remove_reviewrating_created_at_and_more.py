# Generated by Django 4.1.7 on 2023-03-31 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewrating',
            name='created_at',
        ),
        migrations.AddField(
            model_name='reviewrating',
            name='updated_at',
            field=models.DateField(auto_now=True),
        ),
    ]
