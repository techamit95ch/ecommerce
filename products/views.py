from django.http import Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic import ListView, DetailView
from .models import Product
from cart.models import Cart

# Create your views here.
# Featured Product Views Here
class ProductFeaturedListView(ListView):
    queryset = Product.objects.featured()
    template_name = "products/featured-list.html"


class ProductFeaturedDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = "products/featured-details.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        # return Product.objects.featured()
        # Similarly we can write this now
        return Product.objects.all().featured()


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = "products/list.html"
    # """
    # object_list is the parameter we looking for
    # """

    # print(queryset)
    # def get_context_data(self, *args, **kwargs):
    #    context = super(ProductListView,self).get_context_data(*args, **kwargs)
    #    # print(context)
    #    return context

    # get_context_data()


class ProductDetailView(DetailView):
    # queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)

        # print(context)
        # context['abc']=123
        return context

    def get_object(self, *args, **kwargs):
        # Using Custom Query
        request = self.request
        num = self.kwargs.get('num')
        # print("number : ",num)
        instance = Product.objects.get_by_id(num)
        # print(instance)
        # querySet = Product.objects.all()
        if instance is None:
            raise Http404("Product not found")
        return instance

def producDetailView(request, num=None, *args, **kwargs):
    # Here num is a parameter holds primary key
    # print(args)
    # print(kwargs)
    # instance = Product.objects.get(id=num)

    # Here we can do this using 404 error also
    # instance = get_object_or_404(Product,pk=num)

    # Now using try except block
    # try:
    #     instance = Product.objects.get(id=num)
    # except Product.DoesNotExist:
    #     print('Product Does not exist')
    #     raise Http404("Product not found")
    # except:
    #     print("exceptional error")

    # Using Custom Query
    instance = Product.objects.get_by_id(num)
    # print(instance)
    # querySet = Product.objects.all()
    if instance is None:
        raise Http404("Product not found")

    context = {
        'object': instance
    }
    return render(request, "products/detail.html", context)


def productListView(request):
    querySet = Product.objects.all()
    context = {
        'object_list': querySet
    }
    return render(request, "products/list.html", context)


# For slug wise product view

class ProductSlugDetailView(DetailView):
    # queryset = Product.objects.all()
    template_name = "products/detail.html"

    #
    def get_context_data(self, *args, **kwargs):
        context = super(ProductSlugDetailView, self).get_context_data(*args, **kwargs)
        request = self.request

        cart_obj, new_obj = Cart.objects.new_or_get(request) # because we have two objects coming back
        context['cart']= cart_obj
        return context

    def get_object(self, *args, **kwargs):
        # Using Custom Query
        request = self.request
        slug = self.kwargs.get('slug')
        # print(slug)
        try:
            instance = Product.objects.get(slug=slug, active=True)
            # print(instance)
        except Product.DoesNotExist:
            raise Http404("Not Found")
        # To get first object only if multiple objects exists
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Error many")
        return instance
