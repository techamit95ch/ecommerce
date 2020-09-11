from django.db import models

from cart.models import Cart


ORDER_STATUS_CHOICES= (
	('created', 'Created'),
	('paid', 'Paid'),
	('pending', 'Pending'),
	('shipped', 'Shipped'),
	('refunded', 'Refunded')
	)


# Create your models here.
class Orders (models.Model):
    # billing_address = 
    order_id = models.CharField(max_length=120)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    status = models.CharField(max_length=120, default='created')
    shipping_total = models.DecimalField(default= 5.99, max_digits=100, decimal_places=2)
    total = models.DecimalField(default= 0, max_digits=100, decimal_places=2)

    def __str__(self):
    	return self.order_id
