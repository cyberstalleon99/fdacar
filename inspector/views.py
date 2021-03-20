from django.shortcuts import render
from django.views.generic import (
    DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from accounts.models import User
from records.models import Inspection

class InspectorProfileView(LoginRequiredMixin, DetailView):
    template_name = 'inspector/index.html'
    context_object_name = 'inspector'

    def get_object(self):
        user_id =self.kwargs.get("id")
        return get_object_or_404(User, id=user_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curr_user = User.objects.get(pk=self.kwargs.get('id'))
        inspections = ''
        try:
            inspections = Inspection.objects.filter(est_inspectors__inspector=curr_user).distinct()
        except:
            pass
        else:
            inspections = inspections

        # context['qualified_persons'] = curr_user.qualifiedperson_set.filter(status='Active')
        # context['masterlist_active'] = "active"
        context['inspections'] = inspections
        return context
