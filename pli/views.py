from django.views.generic import (
    ListView
)
from .models import Pli
from django.contrib.auth.mixins import LoginRequiredMixin

class PliListView(LoginRequiredMixin, ListView):
    model = Pli
    template_name = 'pli/index.html'
    context_object_name = 'plis'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pli_active'] = "active"
        return context

