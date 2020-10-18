from django.shortcuts import render, redirect
from accounts.forms import LoginForm,GuestForm
from .models import Cart, Product
from orders.models import Order
from billing.models import Billing
from accounts.models import GuestEmail

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)  # because we have two objects coming back

    return render(request, 'cart/home.html', {'cart': cart_obj})


def cart_update(request):
    # print(request.POST.get('product_id'))
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
    if cart_created or cart_obj.products.count == 0:
        return redirect('cart:home')

    # for guest user
    user = request.user
    billing_profile = None
    # print(user.is_authenticated)
    login_form = LoginForm()
    guest_form = GuestForm()

    guest_email_id = request.session.get('guest_email_id')
    if user.is_authenticated:
        # if user.email :
        billing_profile, billing_profile_created = Billing.objects.get_or_create(user=user, email=user.email)
    elif guest_email_id is not None:
        guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
        billing_profile, billing_guest_profile_created = Billing.objects.get_or_create(email=guest_email_obj.email)
    else:
        pass
    # print('\nbilling_profile : ', billing_profile)

    if billing_profile is not None:
        order_obj,order_obj_created=Order.objects.new_or_get(billing_profile,cart_obj)
        # Solved through Order Manager
        # order_qs= Order.objects.filter(billing_profile=billing_profile, cart=cart_obj,active=True)
        # # print('\nbilling_profile : ', billing_profile)
        # # print('\norder_qs : ', order_qs)

        # # if order_qs.exists():
        # if order_qs.count()==1:
        #     order_obj=order_qs.first()
        # else:
        #     # old_order_qs= Order.objects.exclude(billing_profile=billing_profile).filter(cart=cart_obj,active=True)
        #     # if old_order_qs.exists():
        #     #     old_order_qs.update(active=False)
        #     order_obj = Order.objects.create(billing_profile=billing_profile,cart=cart_obj)
        # # else:
        # #     order_obj, new_obj = Order.objects.get_or_create(
        # #             billing_profile=billing_profile,
        # #             cart=cart_obj
        # #         )

    context = {
        "order": order_obj,
        "billing_profile": billing_profile,
        "login_form":login_form,
        "guest_form":guest_form
    }
    # print('\n context : ', context)
    return render(request, 'cart/checkOut.html', context)
