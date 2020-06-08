from django.views.generic import (
    ListView
)
from masterlist.models import Establishment
from masterlist import mypaginator
from .models import Job
# from masterlist.myhelpers import MyExporter
# from .myresources import JobResource
# from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin

class RenewalChekListView(LoginRequiredMixin, ListView):
    model = Establishment
    template_name = 'checklist/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ren_checklist_active'] = "active"
        return context

class PliChekListView(LoginRequiredMixin, ListView):
    model = Establishment
    template_name = 'checklist/pli-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pli_checklist_active'] = "active"
        return context

class RoutineChekListView(LoginRequiredMixin, ListView):
    items_per_page = 10
    model = Establishment
    template_name = 'checklist/routine-list.html'
    context_object_name = 'list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page')
        paginator = mypaginator.MyPaginator(self.get_list(), self.items_per_page, page)
        context['paginated_result'] = paginator.get_paginated_result()
        context['routine_checklist_active'] = "active"
        context['result_count'] = paginator.get_result_count()
        return context

    def get_list(self):
        routine_checklist = Job.routinelist.get_list()
        query = self.request.GET.get('q', None)
        if query:
            routine_checklist = Job.routinelist.get_filtered_list(query=query)
        return routine_checklist

