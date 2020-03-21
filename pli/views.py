from django.shortcuts import render
from django.views.generic import (
    ListView
)
from masterlist.models import Inspection, Establishment

class PLIChekListView(ListView):
    model = Establishment
    template_name = 'pli/index.html'
    context_object_name = 'plichecklist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pli_checklist_active'] = "active"
        return context
