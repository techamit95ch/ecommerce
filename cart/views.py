from django.shortcuts import render,redirect

from .models import Cart,Product
def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request) # because we have two objects coming back
    products = cart_obj.products.all() # fetching all products from cart object in product model
    total = 0
    for x in products:
        total += x.price
    cart_obj.total=total
    cart_obj.save()
    return render(request, 'cart/home.html', {})

def cart_update(request):
    product_id = 'eggs__tss1'
    product_obj = Product.objects.get(slug=product_id)
    cart_obj, new_obj = Cart.objects.new_or_get(request) # because we have two objects coming back
    cart_obj.products.add(product_obj)
    # return redirect('cart:home')
    return redirect(product_obj. get_absolute_url())