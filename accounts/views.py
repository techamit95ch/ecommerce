from django.shortcuts import render
from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from ecommerce.forms import ContactForm, LoginForm, RegisterForm
from django.utils.http import is_safe_url # For saf login



# Create your views here.
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
    if form.is_valid():
        # print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        user0 = authenticate(request, email=username, password=password)

        if user is not None:
            login(request, user)
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
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        newUser = User.objects.create_user(username, email, password)
        print(newUser)
    return render(request, 'accounts/register.html', context)
