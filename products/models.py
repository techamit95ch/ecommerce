import random
import os
from django.db import models
from django.urls import reverse
from django.db.models import Q
from .utils import unique_slug_generator
from django.db.models.signals import pre_save, post_save


# Actually signal is a big model . It has various functions but right we will work with this basic thing only
# reverse utility is for urls

# from django.db import models
# Create your models here.

def getFileNameExt(filepath):
    baseName = os.path.basename(filepath)
    name, ext = os.path.splitext(baseName)
    # print("\n from  getFileNameExt baseName: ", baseName)
    # print("\n from  getFileNameExt name: ",name)
    # print("\n from  getFileNameExt ext: ", ext)
    return name, ext


def uploadImagePath(instance, fileName):
    # print("\n from uploadImagePath instance:", instance)
    # print("\n from uploadImagePath fileName:", fileName)

    newFileName = random.randint(1, 305067012)
    name, ext = getFileNameExt(fileName)
    # for older version python, python3.6 > version
    # finaFileName = '{newFileName}{ext}'.format(newFileName=newFileName,ext=ext)
    # if you are using python3.6 <= version
    finalFileName = f'{newFileName}{ext}'  # .format(newFileName=newFileName, ext=ext)

    # print("\n from uploadImagePath newFileName:", newFileName)
    # print("\n from uploadImagePath finalFileName:", finalFileName)

    return "products/{newFileName}/{finaFileName}".format(
        newFileName=newFileName,
        finaFileName=finalFileName
    )


# for installing python library in your system enter the command:
# pip install pillow

# vid 3.8 9.42

# Well this Model holds some special queryset . Basically its for playing with queryset conjunction

class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True, active=True)

    def search(self, query):
        lookups = (
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(price__icontains=query) |
                Q(tag__title__icontains=query)  # suppose if there is a foreign key named as tag

        )
        # suppose if there is a foreign key named as tag
        # Q(tag__title__icontains=query)
        return self.filter(lookups).distinct()


# For own product manger for custom query set, may useful in some cases
class ProductManager(models.Manager):
    # custom function for get products by id.
    # there self.get_queryset() portion is taking Product.objects
    # Connecting queries with ProductQuerySet

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    # For all active products
    def all(self):
        return self.get_queryset().active()

    # To get Featured Query Set
    def featured(self):
        return self.get_queryset().featured()

    def feature(self):
        # Here it returns those products where featured = True
        return self.get_queryset().filter(featured=True)

    # To Get Product using Id only
    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        # lookups = Q(title__icontains=query) | Q(description__icontains=query)
        # return self.get_queryset().active().filter(lookups).ditinct()
        # after adding search method in ProductQuerySet
        # we can we dont have to filter separately
        # we can simply put search method directly instead of filter
        return self.get_queryset().active().search(query)


class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=19, default=00)
    # For Any File models..FileField was enough
    # image = models.FileField(upload_to=uploadImagePath, null=True, blank=True)
    # For images only field models.ImageField is Required
    image = models.ImageField(upload_to=uploadImagePath, null=True, blank=True)
    # For featured model purpose
    featured = models.BooleanField(default=False)
    # Some times we need products for availability or other purpose
    active = models.BooleanField(default=True)

    # For User friendly pretty urls
    slug = models.SlugField(blank=True, unique=True)
    # Time stamp was not given earlier but it is important Every database should have this
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        # return "/product/{slug}/".format(slug=self.slug)
        return reverse("products:detail", kwargs={'slug': self.slug})
        # it;s similar to previous return but now using reverse detail naming we can g

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    objects = ProductManager()


# after writing  model run (python manage.py makemigration) to create this model
# then migrate
def product_pre_save_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_reciever, sender=Product)
