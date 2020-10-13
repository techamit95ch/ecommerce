from django.conf import settings
from django.db import models
from django.db.models.signals import post_save

User = settings.AUTH_USER_MODEL
# PASSWORD = settings.AUTH_USER_MODEL


# Create your models here.
class Billing(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    email = models.EmailField(null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


# def billing_profile_created_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         BillingProfile.objects.get_or_create(user=instance)
#         instance.

def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        Billing.objects.get_or_create(user=instance,email=instance.email)


post_save.connect(user_created_receiver, sender=User)
