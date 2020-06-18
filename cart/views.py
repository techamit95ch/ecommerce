from django.shortcuts import render

from .models import Cart


# Create your views here.
def cart_home(request):
    # print(request.session.session_key) # on the request
    # request.session['cart_id']=13
    # to save username in session varriable
    # request.session['username']= request.user.username
    # print(request.session.get('username'))
    # Deleteing cart id session varriable
    del request.session['cart_id']

    cart_id = request.session.get("cart_id", None)
    # if cart_id doesn't exist in session then it will responce None. not error.

    if cart_id is None:  # and isinstance(cart_id,int):
        # print('create new cart')
        cart_obj = Cart.objects.create(user=None)
        request.session['cart_id'] = cart_obj.id
    else:
        print(cart_id)
        cart_obj = Cart.objects.get(id=cart_id)
        # print("cart id exists")

    return render(request, 'cart/home.html', {})
