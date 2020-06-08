from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from products.views import ProductListView
from .views import SearchProductView

app_name = 'search'

urlpatterns = [

    path('', SearchProductView.as_view(), name='query'),

]
