from django.db import models
from django.conf import settings
from products.models import Product
from django.db.models.signals import pre_save, post_save,m2m_changed

User = settings.AUTH_USER_MODEL


# Create your models here.
class CartManager(models.Manager):
    # def get_or_create():
    #     return obj,True
    def new(self, user=None):
        user_obj = None
        if user is not None and user.is_authenticated:
            user_obj= user

        return self.model.objects.create(user=user_obj)
        
    def new_or_get(self,request):
        cart_id = request.session.get("cart_id", None) # getting session cart id
        qs = self.get_queryset().filter(id=cart_id) # getting all objects form the Cart
        
        if qs.count() == 1: # here it means user just adding cart for the first time
            new_obj = False # as because not new cart object got
            cart_obj = qs.first() # fetching only first object
            # print(request.user.is_authenticated == True)
            if request.user.is_authenticated and cart_obj.user is None : #for the first time entry for that user
                
                cart_obj.user = request.user # adding that user in cart object
                cart_obj.save() # saveing all details in cart object
        else:
            cart_obj = Cart.objects.new(user= request.user) # creating new object with according user who already logged in and has many product in the cart 
            new_obj =True # yes it new objectConnection
            # if user.is_authenticated:
            #     user_obj = user
            request.session['cart_id']=cart_obj.id
        return cart_obj,new_obj


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True, null=True)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    sub_total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)
    
    


def m2m_changed_cart_reciever(sender, instance, action, *args, **kwargs):
   
    if action  in ['post_add','post_remove','post_clear']:
        
        products = instance.products.all() # fetching all products from cart object in product model
        
        total = 0
        for x in products:
            total += x.price
        
        if instance.sub_total != total:
            instance.sub_total=total
            instance.save()
# m2m_changed is a singnal used save while using many 2 many connection field setup
m2m_changed.connect(m2m_changed_cart_reciever,sender=Cart.products.through)

def pre_save_cart_reciever(sender, instance, *args, **kwargs):
    # print(action)
    gst =10
    instance.total= instance.sub_total + gst

pre_save.connect(pre_save_cart_reciever,sender=Cart)