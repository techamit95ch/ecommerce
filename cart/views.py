from django.shortcuts import render, redirect

from .models import Cart, Product
from orders.models import Order


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)  # because we have two objects coming back

    return render(request, 'cart/home.html', {'cart': cart_obj})


def cart_update(request):
    print(request.POST.get('product_id'))
    product_id = request.POST.get('product_id')
    if product_id is not None:

        product_obj = Product.objects.get(id=product_id)
        cart_obj, new_obj = Cart.objects.new_or_get(request)  # because we have two objects coming back
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
        else:
            cart_obj.products.add(product_obj)
        request.session['cart_items'] = cart_obj.products.count()
    return redirect('cart:home')
    # return redirect(product_obj. get_absolute_url())
    # 10


def checkoutHome(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if not cart_created or cart_obj.products.count != 0:
        order_obj, new_obj = Order.objects.get_or_create(cart=cart_obj)
    else:
        return redirect('cart:home')
    return render(request, 'cart/checkOut.html', {"order": order_obj})
