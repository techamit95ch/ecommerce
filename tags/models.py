from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save, post_save
from products.models import Product
from products.utils import unique_slug_generator


# Actually signal is a big model . It has various functions but right we will work with this basic thing only


# Create your models here.
class Tag(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField()
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    products = models.ManyToManyField(Product, blank=True)  # Actually this is for foreign key

    def __str__(self):
        return self.title


def tag_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(tag_pre_save_receiver, sender=Tag)

# Right now it's
# vid 6 03.46
