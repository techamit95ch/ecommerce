from django.shortcuts import render
from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ContactForm, LoginForm, RegisterForm,GuestForm
from django.utils.http import is_safe_url # For safe login
from .models import GuestEmail


# Create your views here.
def guest_login_view(request):
    form = GuestForm(request.POST or None)
    # print(request.user.is_authenticated)
    context = {
        "form": form
    }
    # To check For The next Url...
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None

    # print("\n redirect path == ",redirect_path)

    if form.is_valid():
        email = form.cleaned_data.get('email')
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id']= new_guest_email.id
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect('/register/')
    return redirect('/register/')

def login_Page(request):
    form = LoginForm(request.POST or None)
    # print(request.user.is_authenticated)
    context = {
        "form": form
    }
    # To check For The next Url...
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post
    # print("\n redirect path == {} \n",redirect_path)
    # print(redirect_path)
    # print("\n")
    if form.is_valid():
        # print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        # user0 = authenticate(request, email=username, password=password)

        if user is not None:
            login(request, user)
            try:
                del request.session['guest_email_id']
            except :
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('/')


            # print('USER LOGGED IN ')
            # Redirect to a success page.
            # context["form"] = LoginForm()
            return redirect('/admin')
        else:
            # Return an 'invalid login' error message.
            # print(user0)
            print("Error")

        # context["form"] = LoginForm()

    return render(request, 'accounts/login.html', context)


User = get_user_model()


def registerPage(request):
    form = RegisterForm(request.POST or None)
    # print(request.user.is_authenticated)
    context = {
        "form": form
    }

    if form.is_valid():
        # print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        newUser = User.objects.create_user(username, email, password)
        # print(newUser)
    return render(request, 'accounts/register.html', context)
