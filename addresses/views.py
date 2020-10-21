from django.shortcuts import render, redirect
from django.utils.http import is_safe_url  # For safe login
from billing.models import Billing
from .forms import AddressForm
from .models import Address
# Create your views here.


def checkout_address_create_view(request):
    form = AddressForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        # print(request.POST)
        instance = form.save(commit=False)
        billing_profile, billing_profile_created = Billing.objects.new_or_get(
            request)
        if billing_profile is not None:
            instance.billing_profile = billing_profile
            address_type = request.POST.get(
                'address_type', 'shipping')
            instance.address_types = address_type
            instance.save()
            # print('======= address_type  ========', address_type)
            request.session[address_type+'_address_id'] = instance.id
            # billing_address_id = request.session.get(
            #     'billing_address_id', None)
            # shipping_address_id = request.session.get(
            #     'shipping_address_id', None)
            # print(address_type+'_address_id')
        else:
            # print("error")
            return redirect('cart:checkout')
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
    return redirect('cart:checkout')

def checkout_address_use_view(request):
    if request.user.is_authenticated:
        context = { }
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        if request.method == 'POST':
            shipping_address = request.POST.get('shipping_address',None)
            billing_address = request.POST.get('billing_address',None)
            billing_profile, billing_profile_created = Billing.objects.new_or_get(request)
            address_type = request.POST.get('address_type', 'shipping')
            if shipping_address is not None:
                qs= Address.objects.filter(billing_profile=billing_profile,id=shipping_address)
                if qs.exists():
                    print(address_type+'_address_id')
                    request.session[address_type+'_address_id'] = shipping_address
                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)
            elif billing_address is not None:
                qs= Address.objects.filter(billing_profile=billing_profile,id=billing_address)
                if qs.exists():
                    print(address_type+'_address_id')
                    request.session[address_type+'_address_id'] = billing_address
                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)

        return redirect('cart:checkout')
