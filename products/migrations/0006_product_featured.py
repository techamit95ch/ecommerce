# Generated by Django 3.0.3 on 2020-05-26 13:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('products', '0005_auto_20200519_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='featured',
            field=models.BooleanField(default=False),
        ),
    ]
