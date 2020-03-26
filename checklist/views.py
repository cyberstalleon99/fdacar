from django.shortcuts import reverse
from django.views.generic import (
    ListView
)
from django.http import HttpResponseRedirect
from masterlist.models import Establishment

class RenewalChekListView(ListView):
    model = Establishment
    template_name = 'checklist/index.html'
    context_object_name = 'list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['renewalchecklist'] = Establishment.renchecklist.get_list()
        context['ren_checklist_active'] = "active"
        return context

class PliChekListView(ListView):
    model = Establishment
    template_name = 'checklist/index0.html'
    context_object_name = 'list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['renewalchecklist'] = Establishment.plichecklist.get_list()
        context['pli_checklist_active'] = "active"
        print('PliChekListView(ListView)')
        return context
