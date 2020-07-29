from django.views.generic import (
    ListView
)
from .models import Outgoing
from django.contrib.auth.mixins import LoginRequiredMixin

class OutgoingListView(LoginRequiredMixin, ListView):
    model = Outgoing
    template_name = 'outgoing/index.html'
    context_object_name = 'outgoings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['outgoing_active'] = "active"
        return context

