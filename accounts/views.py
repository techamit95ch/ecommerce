from django.shortcuts import render
from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from ecommerce.forms import ContactForm, LoginForm, RegisterForm


# Create your views here.
def login_Page(request):
    form = LoginForm(request.POST or None)
    # print(request.user.is_authenticated)
    context = {
        "form": form

    }


    if form.is_valid():
        # print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        user0 = authenticate(request, email=username, password=password)

        if user is not None:
            login(request, user)
            # print('USER LOGGED IN ')
            # Redirect to a success page.
            # context["form"] = LoginForm()
            return redirect('/admin')
        else:
            # Return an 'invalid login' error message.
            # print(user0)
            print("Error")

        # context["form"] = LoginForm()

    return render(request, 'auth/login.html', context)


User = get_user_model()


def registerPage(request):
    form = RegisterForm(request.POST or None)
    # print(request.user.is_authenticated)
    context = {
        "form": form
    }

    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        newUser = User.objects.create_user(username, email, password)
        print(newUser)
    return render(request, 'auth/register.html', context)
