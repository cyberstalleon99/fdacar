from django.shortcuts import reverse
from django.views.generic import (
    ListView
)
from django.http import HttpResponseRedirect
from masterlist.models import Establishment, SpecificActivity
from masterlist import mypaginator
from .models import Job

class RenewalChekListView(ListView):
    items_per_page = 10
    model = Establishment
    template_name = 'checklist/index.html'
    context_object_name = 'list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page')
        paginator = mypaginator.MyPaginator(self.get_list(), self.items_per_page, page)
        context['paginated_result'] = paginator.get_paginated_result()
        context['ren_checklist_active'] = "active"
        return context

    def get_list(self):
        renewal_checklist = Job.renchecklist.get_list()
        query = self.request.GET.get('q', None)
        if query:
            renewal_checklist = Job.renchecklist.get_filtered_list(query=query)
        return renewal_checklist

class PliChekListView(ListView):
    items_per_page = 10
    model = Establishment
    template_name = 'checklist/pli-list.html'
    context_object_name = 'list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page')
        paginator = mypaginator.MyPaginator(self.get_list(), self.items_per_page, page)
        context['paginated_result'] = paginator.get_paginated_result()
        context['pli_checklist_active'] = "active"
        return context

    def get_list(self):
        pli_checklist = Job.plichecklist.get_list()
        query = self.request.GET.get('q', None)
        if query:
            pli_checklist = Job.plichecklist.get_filtered_list(query=query)

        return pli_checklist

class RoutineChekListView(ListView):
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
        return context

    def get_list(self):
        routine_checklist = Job.routinelist.get_list()
        query = self.request.GET.get('q', None)
        if query:
            routine_checklist = Job.routinelist.get_filtered_list(query=query)
        return routine_checklist
