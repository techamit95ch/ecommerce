from django.db import models
from django.db.models.signals import pre_save ,post_save
from cart.models import Cart
from ecommerce.utils import unique_order_id_generator
import math
ORDER_STATUS_CHOICES= (
	('created', 'Created'),
	('paid', 'Paid'),
	('pending', 'Pending'),
	('shipped', 'Shipped'),
	('refunded', 'Refunded')
	)


# Create your models here.
class Order (models.Model):
    # billing_address = 
    order_id = models.CharField(max_length=120)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    status = models.CharField(max_length=120, default='created')
    shipping_total = models.DecimalField(default= 5.99, max_digits=100, decimal_places=2)
    total = models.DecimalField(default= 0, max_digits=100, decimal_places=2)

    

    def __str__(self):
    	return self.order_id

    def update_total(self):
        cart_total=self.cart.total
        cart_shipping_total = self.shipping_total
        total = format( math.fsum([ cart_total , cart_shipping_total]),'.2f'); 
        self.total= total
        self.save()
        return total

def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id= unique_order_id_generator(instance)

pre_save.connect(pre_save_create_order_id,  sender=Order)

def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs= Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()

post_save.connect(post_save_cart_total, sender=Cart)
# post_save.connect()
def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()
post_save.connect(post_save_order, sender=Order)