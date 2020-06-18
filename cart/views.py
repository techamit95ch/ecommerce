from django.shortcuts import render

from .models import Cart


# Create your views here.

def cart_create(user=None):
    cart_obj = Cart.objects.create(user=None)
    return cart_obj


def cart_home(request):
    del request.session['cart_id']

    cart_id = request.session.get("cart_id", None)
    # if cart_id is None:  # and isinstance(cart_id,int):
    #     cart_obj = Cart.objects.create(user=None)
    #     request.session['cart_id'] = cart_obj.id
    # else:
    #     # print(cart_id)
    qs = Cart.objects.filter(id=cart_id)
    if qs.count() == 1:
        cart_obj = qs.first()
    else:

        # cart_obj = cart_create()
        cart_obj = Cart.objects.new(user=None)
    request.session['cart_id'] = cart_obj.id
    return render(request, 'cart/home.html', {})
