from django.contrib import admin

# Register your models here.
from .models import Product


# Register Product to Admin Site

# this class ProductAdmin meant to use for slug url views
class ProductAdmin(admin.ModelAdmin):
    # Displaying lists
    list_display = ['__str__', 'slug']

    class Meta:
        model = Product


admin.site.register(Product, ProductAdmin)
