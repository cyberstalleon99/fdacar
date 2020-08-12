from django.views.generic import (
    ListView
)
from .models import Application
from django.contrib.auth.mixins import LoginRequiredMixin

class ApplicationListView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'appsreceived/index.html'
    context_object_name = 'applications'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['apps_active'] = "active"
        return context
