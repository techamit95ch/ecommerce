from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ContactForm, LoginForm


def home_page(request):
    context = {
        "title": "Home Page",
        "content": " jdksd ksdnksdn"
    }
    return render(request, "home_page.html", context)


def about_page(request):
    context = {
        "title": "About Page",
        "content": " jdksd ksdnksdn"
    }
    return render(request, "home_page.html", context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title": "Contact",
        "content": "This Is Contact Page",
        "form": contact_form
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
    if request.method == "POST":
        print(request.POST.get('fullName'))
    return render(request, "contact/view.html", context)


def login_Page(request):
    form = LoginForm(request.POST or None)
    print(request.user.is_authenticated)
    context = {
        "form": form
    }


    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print('USER LOGGED IN ')
            # Redirect to a success page.
            # context["form"] = LoginForm()
            return redirect('/login')
        else:
            # Return an 'invalid login' error message.
            print("Error")

        context["form"] = LoginForm()

    return render(request, 'auth/login.html', context)


def registerPage(request):
    return render(request, 'auth/register.html', {})
