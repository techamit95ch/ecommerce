from django.shortcuts import render

from .models import Cart


# Create your views here.

# def cart_create(user=None):
#     cart_obj = Cart.objects.create(user=None)
#     return cart_obj


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request) # because we have two objects coming back
    products = cart_obj.products.all() # fetching all products from cart object in product model
    # now we will work on total which we can see in the cart panel of the main admin  panel
    print('--------------------cart object is: ----------------------')

    print(cart_obj)
    print('-----------------')
    total = 0
    for x in products:
        total += x.price
    print('\ntotal is:---',total)
    cart_obj.total=total
    cart_obj.save()
    return render(request, 'cart/home.html', {})
