# Generated by Django 3.1.2 on 2020-10-12 01:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0004_auto_20201012_0715'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billing',
            name='user',
        ),
    ]
