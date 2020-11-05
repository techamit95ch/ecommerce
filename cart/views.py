from django.shortcuts import render, redirect
from django.http import JsonResponse
from accounts.forms import LoginForm, GuestForm
from .models import Cart, Product
from orders.models import Order
from billing.models import Billing
from accounts.models import GuestEmail
from addresses.forms import AddressForm
from addresses.models import Address


def cart_api_update(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [{"name": x.name, "price": x.price}
                for x in cart_obj.products.all()]
    cart_data = {'products': products,
                 "sub_total": cart_obj.sub_total, "total": cart_obj.total}
    return JsonResponse(cart_data)


def cart_home(request):
    # because we have two objects coming back
    cart_obj, new_obj = Cart.objects.new_or_get(request)

    return render(request, 'cart/home.html', {'cart': cart_obj})


def cart_update(request):
    product_id = request.POST.get('product_id')
    # print(product_id)
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Error! Product Gone")
        # print(product_obj)
        # because we have two objects coming back
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        #
        cart_obj.products.all()
        product_added = False
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            product_added = False

        else:
            cart_obj.products.add(product_obj)
            # cart_obj.products.all()
            product_added = True
        # print(cart_obj.products.all())
        request.session['cart_items'] = cart_obj.products.count()
        if request.is_ajax():
            json_data = {
                'added': product_added,
                'removed': not product_added,
                '_count': cart_obj.products.count(),
                'api': 'api/'
            }
            return JsonResponse(json_data , status =200)
            # return JsonResponse({"message":"Error 400"} , status_code=500)
            # print('\noh my fuck! Its ajax')
    return redirect('cart:home')


def checkoutHome(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count == 0:
        return redirect('cart:home')
    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    # billing_address_form = AddressForm()
    billing_address_id = request.session.get('billing_address_id', None)
    shipping_address_id = request.session.get('shipping_address_id', None)
    billing_profile, billing_profile_created = Billing.objects.new_or_get(
        request)
    address_qs = None
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(
                billing_profile=billing_profile)
        #
        # shipping_addres_qs = address_qs.filter(address_type='shipping')
        # billing_addres_qs = address_qs.filter(address_type='billing')
        # address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(
            billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(
                id=shipping_address_id)
            del(request.session['shipping_address_id'])
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(
                id=billing_address_id)
            del(request.session['billing_address_id'])
        if billing_address_id or shipping_address_id:
            order_obj.save()
    if request.method == 'POST':

        is_done = order_obj.check_done()
        if is_done:
            order_obj.mark_paid()
            del(request.session['cart_id'])
            request.session['cart_items'] = 0
        return redirect('cart:success')

        # pass
    # print(address_qs)
    context = {
        "order": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        "address_qs": address_qs
        # "billing_address_form": billing_address_form,
    }
    # print(context)
    return render(request, 'cart/checkOut.html', context)


def success(request):
    return redirect('home')
    # pass
