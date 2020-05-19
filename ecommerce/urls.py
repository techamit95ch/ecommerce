"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import home_page, contact_page, login_Page, registerPage
from products.views import productListView, ProductListView, ProductDetailView, producDetailView
urlpatterns = [
    path('', home_page),
    path('contact/', contact_page),
    path('login/', login_Page),
    path('register/', registerPage),
    path('product/', ProductListView.as_view()),
    path('product-fv/', productListView),
    path('product/<int:num>/', ProductDetailView.as_view()),  # Api for product details indevidually
    # here slug pk must be the param name that model expecting to have
    path('product-fv/<int:num>/', producDetailView),  # Api for product details individually, And its ideal way to
    # to represent url

    path('admin/', admin.site.urls),

]

if settings.DEBUG:
    # set static files
    # print(settings.MEDIA_ROOT)
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # type python manage.py collectstatic
