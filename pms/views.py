from django.views.generic import (
    ListView
)
from .models import Product
from django.contrib.auth.mixins import LoginRequiredMixin

class PmsListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'pms/index.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pms_active'] = "active"
        return context