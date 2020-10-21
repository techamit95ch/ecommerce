from django.db import models
from django.db.models.signals import pre_save, post_save
from cart.models import Cart
from ecommerce.utils import unique_order_id_generator
from billing.models import Billing
from addresses.models import Address
import math

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('pending', 'Pending'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded')
)


# Create your models here.

class OrderManager(models.Manager):
    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset().filter(
            billing_profile=billing_profile, cart=cart_obj, active=True)
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(
                billing_profile=billing_profile, cart=cart_obj)
            created = True
        return obj, created


class Order(models.Model):
    billing_profile = models.ForeignKey(
        Billing, null=True, blank=True, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=120)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=120, default='created')
    shipping_total = models.DecimalField(
        default=5.99, max_digits=100, decimal_places=2)
    shipping_address = models.ForeignKey(
        Address, on_delete=models.CASCADE, null=True, blank=True, related_name="shipping_address")
    billing_address = models.ForeignKey(
        Address, on_delete=models.CASCADE, null=True, blank=True, related_name="billing_address")

    total = models.DecimalField(default=0, max_digits=100, decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.order_id
    objects = OrderManager()

    def update_total(self):
        cart_total = self.cart.total
        cart_shipping_total = self.shipping_total
        total = math.fsum([cart_total, cart_shipping_total])
        f_total = format(total, '.2f')
        self.total = total
        self.save()
        return total

    def check_done(self):
        billing_profile = self.billing_profile
        shipping_address = self.shipping_address
        billing_address = self.billing_address
        total = self.total
        if billing_profile and billing_address and shipping_address and total > 0:
            return True
        return False

    def mark_paid(self):
        if self.check_done():
            self.status = 'paid'
            self.save()
            return self.status


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(
        billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)


pre_save.connect(pre_save_create_order_id, sender=Order)


def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()


post_save.connect(post_save_cart_total, sender=Cart)


# post_save.connect()
def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()
    # instance.update_total()


post_save.connect(post_save_order, sender=Order)
