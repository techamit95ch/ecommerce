from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from django.db.models import Q
from products.models import Product


class SearchProductView(ListView):
    # queryset = Product.objects.filter(title__icontains='Eggs')
    template_name = "search/view.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        query = request.GET.get('q', None)
        if query is not None:
            # This Q model provide multiple field selection option
            # lookups= Q(title__icontains=query)| Q(description__icontains=query)
            # return Product.objects.filter(lookups).distinct()
            return Product.objects.search(query)
        else:
            return Product.objects.featured()

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super(SearchProductView, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        # SearchQuery.objects.create(query=query)
        return context

    #     vid 3 08.00
    # def get_queryset(self, *args, **kwargs):
    #     # Using Custom Query
    #     request = self.request
