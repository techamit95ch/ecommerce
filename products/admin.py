from django.contrib import admin

# Register your models here.
from .models import Product

# Register Product to Admin Site
admin.site.register(Product)
