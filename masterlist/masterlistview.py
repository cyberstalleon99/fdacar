from django.views.generic import ListView
from .models import Establishment
from . import mypaginator
from django.db.models import Q

class MasterListView(ListView):
    model = Establishment
    items_per_page = 10
    context_object_name = 'establishments'
    establishments = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page')
        paginator = mypaginator.MyPaginator(self.get_establishments(), self.items_per_page, page)
        establishments = paginator.get_paginated_result()
        context['paginated_result'] = establishments
        context['result_count'] = paginator.get_result_count()
        return context

    def init_establishments(self, establishments):
        self.establishments = establishments

    def get_establishments(self):
        establishments = self.establishments
        query = self.request.GET.get('q', None)
        if query:
            establishments = self.establishments.filter(
                Q(name__icontains=query) |
                Q(plant_address__address__icontains=query) |
                Q(plant_address__municipality_or_city__name__icontains=query) |
                Q(plant_address__region__name__icontains=query) |
                Q(plant_address__province__name__icontains=query) |
                Q(product_type__name__icontains=query) |
                Q(primary_activity__name__icontains=query) |
                Q(specific_activity__name__icontains=query) |
                Q(ltos__lto_number__icontains=query)
            ).distinct()
        return establishments
