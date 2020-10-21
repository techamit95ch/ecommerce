from django.db import models
from billing.models import Billing
# Create your models here.
ADDRESS_TYPES = (
    ('BILLING', 'billing'),
    ('SHIPPING', 'shipping')
)


class Address(models.Model):
    billing_profile = models.ForeignKey(
        Billing, on_delete=models.CASCADE)
    addressLine1 = models.CharField(max_length=100)
    addressLine2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return str(self.billing_profile)
    def get_address(self):
        return "{line1}\n{line2}\n"
