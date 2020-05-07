from django.http import HttpResponse
from django.shortcuts import  render

def home_page(request):
    context = {
        "title": "Home Page",
        "content" : " jdksd ksdnksdn"
    }
    return render(request, "home_page.html", context)
def about_page(request):
    context = {
        "title": "About Page",
        "content": " jdksd ksdnksdn"
    }
    return render(request, "home_page.html", context)
def contact_page(request):
    context = {
        "title": "Contact",
        "content": " jdksd ksdnksdn"
    }
    return render(request, "contact/view.html", context)