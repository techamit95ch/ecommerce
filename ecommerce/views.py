from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from accounts.forms import ContactForm


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
        if  request.is_ajax():
            return JsonResponse({"message":"Sucess"},status=200)
    if contact_form.errors:
        errors= contact_form.errors.as_json()
        return HttpResponse(errors,status=400,content_type='application/json')

    return render(request, "contact/view.html", context)
