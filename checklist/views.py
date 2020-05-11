from django.shortcuts import reverse
from django.views.generic import (
    ListView
)
from django.http import HttpResponseRedirect
from masterlist.models import Establishment, SpecificActivity
from masterlist import mypaginator
from .models import Job
from masterlist.myhelpers import MyExporter
from .myresources import JobResource
from django.utils import timezone
from datetime import datetime

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
        context['result_count'] = paginator.get_result_count()
        return context

    def get_list(self):
        renewal_checklist = Job.renchecklist.get_list()
        query = self.request.GET.get('q', None)
        if query:
            renewal_checklist = Job.renchecklist.get_filtered_list(query=query)
        return renewal_checklist

def export_renewal(request):
    renewal_checklist = Job.renchecklist.get_list()
    query = request.GET.get('q', None)
    if query:
        renewal_checklist = Job.renchecklist.get_filtered_list(query=query)
    response = MyExporter.export_to_xslx(
                                        resource=JobResource(),
                                        filename="Renewal Checklist Pullout as of {}".format(timezone.now().date()),
                                        queryset=renewal_checklist
    )
    return response

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
        context['result_count'] = paginator.get_result_count()
        return context

    def get_list(self):
        pli_checklist = Job.plichecklist.get_list()
        query = self.request.GET.get('q', None)
        if query:
            pli_checklist = Job.plichecklist.get_filtered_list(query=query)
        return pli_checklist

def export_pli(request):
    pli_checklist = Job.plichecklist.get_list()
    query = request.GET.get('q', None)
    if query:
        pli_checklist = Job.plichecklist.get_filtered_list(query=query)
    response = MyExporter.export_to_xslx(
                                        resource=JobResource(),
                                        filename="PLI List Pullout as of {}".format(timezone.now().date()),
                                        queryset=pli_checklist
    )
    return response

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
        context['result_count'] = paginator.get_result_count()
        return context

    def get_list(self):
        routine_checklist = Job.routinelist.get_list()
        query = self.request.GET.get('q', None)
        if query:
            routine_checklist = Job.routinelist.get_filtered_list(query=query)
        return routine_checklist

def export_routine(request):
    routine_checklist = Job.routinelist.get_list()
    query = request.GET.get('q', None)
    if query:
        routine_checklist = Job.routinelist.get_filtered_list(query=query)
    response = MyExporter.export_to_xslx(
                                        resource=JobResource(),
                                        filename="Routine List Pullout as of {}".format(timezone.now().date()),
                                        queryset=routine_checklist
    )

    return response
