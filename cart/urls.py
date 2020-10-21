from django.urls import path
from cart.views import (
    cart_home,
    cart_update,
    Cart,
    checkoutHome,
    success
)

# If you are using namespace in main url in include then providing this app_name is necessary
app_name = 'cart'
urlpatterns = [

    path('', cart_home, name='home'),
    path('update', cart_update, name='update'),
    path('checkout', checkoutHome, name='checkout'),
    path('success', success, name='success'),
]
