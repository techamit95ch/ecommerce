from django.urls import path
from products.views import (
    # productListView,
    ProductListView,
    ProductDetailView,
    # producDetailView,
    # ProductFeaturedListView,
    # ProductFeaturedDetailView,
    ProductSlugDetailView
)

# If you are using namespace in main url in include then providing this app_name is necessary
app_name = 'products'
urlpatterns = [

    path('', ProductListView.as_view(), name='list'),
    # path('product-fv/', productListView),
    path('<int:num>/', ProductDetailView.as_view()),  # Api for product details individually
    # # here slug pk must be the param name that model expecting to have
    # path('product-fv/<int:num>/', producDetailView),  # Api for product details individually, And its ideal way to
    # # to represent url
    #
    # # Featured product path
    # path('featured/', ProductFeaturedListView.as_view()),
    #
    # # Here ProductFeaturedDetailView expect this query name as pk object as a variable name or slug variable
    # path('featured/<int:pk>/', ProductFeaturedDetailView.as_view()),  # Api for product details individually

    # Slug or non primary key attribute url
    path('<slug:slug>/', ProductSlugDetailView.as_view(), name='detail'),

]
