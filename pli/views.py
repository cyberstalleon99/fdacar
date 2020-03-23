from django.shortcuts import reverse
from django.views.generic import (
    ListView
)
from django.http import HttpResponseRedirect
from masterlist.models import Establishment

class PLIChekListView(ListView):
    model = Establishment
    template_name = 'pli/index.html'
    context_object_name = 'list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plichecklist'] = Establishment.plichecklist.get_list()
        context['pli_checklist_active'] = "active"
        return context
