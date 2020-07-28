from django.views.generic import (
    ListView
)
from .models import Incoming
from django.contrib.auth.mixins import LoginRequiredMixin

class IncomingListView(LoginRequiredMixin, ListView):
    model = Incoming
    template_name = 'incoming/index.html'
    context_object_name = 'incomings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['incoming_active'] = "active"
        return context

