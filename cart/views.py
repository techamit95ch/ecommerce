from django.shortcuts import render

# Create your views here.
def cart_home(request):
    # print(request.session.session_key) # on the request
    request.session['cart_id']=13
    # to save username in session varriable
    request.session['username']= request.user.username
    # print(request.session.get('username'))
    return render(request,'cart/home.html',{})