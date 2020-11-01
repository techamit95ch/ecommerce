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
from django.urls import path, include
from .views import home_page, contact_page
from accounts.views import login_Page, registerPage, guest_login_view
from addresses.views import checkout_address_create_view,checkout_address_use_view
from cart.views import cart_api_update
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # here this name is important  during navigation, we don't have to type that url
    path('', home_page, name='home'),
    # we simply have to recall this given name
    path('contact/', contact_page, name='contact'),
    path('checkout/address/create_view/',checkout_address_create_view, name='checkout_address_create'),
    path('checkout/address/use_view/',checkout_address_use_view, name='checkout_address_use'),

    path('login/', login_Page, name="login"),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register/', registerPage, name="register"),
    path('register/guest/', guest_login_view, name="guest_register"),
    path('admin/', admin.site.urls),
    path('products/', include('products.urls', namespace="products")),
    path('cart/', include('cart.urls', namespace="cart")),
    path('cart/api/', cart_api_update, name=''),
    path('search/', include('search.urls', namespace="search")),
]

if settings.DEBUG:
    # set static files
    # print(settings.MEDIA_ROOT)
    urlpatterns = urlpatterns + \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # type python manage.py collectstatic
