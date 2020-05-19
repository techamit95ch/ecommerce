import random
import os
from django.db import models


# from django.db import models
# Create your models here.

def getFileNameExt(filepath):
    baseName = os.path.basename(filepath)
    name, ext = os.path.splitext(baseName)
    # print("\nfrom  getFileNameExt baseName: ", baseName)
    # print("\nfrom  getFileNameExt name: ",name)
    # print("\nfrom  getFileNameExt ext: ", ext)
    return name, ext


def uploadImagePath(instance, fileName):
    # print("\nfrom uploadImagePath instance:", instance)
    # print("\nfrom uploadImagePath fileName:", fileName)

    newFileName = random.randint(1, 305067012)
    name, ext = getFileNameExt(fileName)
    # for older version python, python3.6 > version
    # finaFileName = '{newFileName}{ext}'.format(newFileName=newFileName,ext=ext)
    # if you are using python3.6 <= version
    finalFileName = f'{newFileName}{ext}'  # .format(newFileName=newFileName, ext=ext)

    # print("\nfrom uploadImagePath newFileName:", newFileName)
    # print("\nfrom uploadImagePath finalFileName:", finalFileName)

    return "products/{newFileName}/{finaFileName}".format(
        newFileName=newFileName,
        finaFileName=finalFileName
    )


# for installing python library in your system enter the command:
# pip install pillow

# vid 3.8 9.42

# For own product manger for custom query set, may useful in some cases
class ProductManager(models.Manager):
    # custom function for get products by id.
    # there self.get_queryset() portion is taking Product.objects

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None


class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=19, default=00)
    # For Any File models..FileField was enough
    # image = models.FileField(upload_to=uploadImagePath, null=True, blank=True)
    # For images only field models.ImageField is Required
    image = models.ImageField(upload_to=uploadImagePath, null=True, blank=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    objects = ProductManager()
# after writing  model run (python manage.py makemigration) to create this model
# then migrate
