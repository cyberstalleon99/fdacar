from django.views.generic import (
    ListView,
    DetailView,
)

from .models import Establishment
from django.utils import timezone
from .myhelpers import MyExporter
from .myresources import EstablishmentResource
from django.shortcuts import get_object_or_404, render
from django.views import View

class AllListView(ListView):
    model = Establishment
    template_name = 'masterlist/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['alllist_active'] = "active"
        context['alllist_tab_active'] = "active"
        return context

class InactiveListView(ListView):
    model = Establishment
    template_name = 'masterlist/inactive-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inactive_tab_active'] = "active"
        context['alllist_active'] = "active"
        return context

    def get_list(self):
        inactivelist = Establishment.inactivelist.get_list()
        query = self.request.GET.get('q', None)
        if query:
            inactivelist = Establishment.inactivelist.get_filtered_list(query=query)
        return inactivelist

class AbraListView(ListView):
    model = Establishment
    template_name = 'masterlist/abra-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['abra_list_active'] = "active"
        return context

class ApayaoListView(ListView):
    model = Establishment
    template_name = 'masterlist/apayao-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['apayao_list_active'] = "active"
        return context

class BaguioListView(ListView):
    model = Establishment
    template_name = 'masterlist/baguio-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['baguio_list_active'] = "active"
        return context

class BenguetListView(ListView):
    model = Establishment
    template_name = 'masterlist/benguet-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['benguet_list_active'] = "active"
        return context

class IfugaoListView(ListView):
    model = Establishment
    template_name = 'masterlist/ifugao-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['ifugao_list_active'] = "active"
        return context

class KalingaListView(ListView):
    model = Establishment
    template_name = 'masterlist/kalinga-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['kalinga_list_active'] = "active"
        return context

class MountainListView(ListView):
    model = Establishment
    template_name = 'masterlist/mountain-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['mountain_list_active'] = "active"
        return context

class ExpiredListView(ListView):
    model = Establishment
    template_name = 'masterlist/expired-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expiredlist_active'] = "active"
        return context

def export_expired(request):
    checklist = Establishment.expiredlist.get_list()
    query = request.GET.get('q', None)
    if query:
        checklist = Establishment.expiredlist.get_filtered_list(query=query)

    response = MyExporter.export_to_xslx(resource=EstablishmentResource(), filename="Expired List Pullout as of {}".format(timezone.now().date()),
    queryset=checklist)
    return response

class EstablishmentDetailView(DetailView):
    template_name = 'masterlist/establishment-detail/establishment-detail.html'
    context_object_name = 'establishment'

    def get_object(self):
        est_id =self.kwargs.get("id")
        return get_object_or_404(Establishment, id=est_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curr_est = Establishment.objects.get(pk=self.kwargs.get('id'))
        context['alllist_active'] = "active"
        inspections = ''
        try:
            curr_est.record # Check if establishment has a record
        except:
            pass
        else:
            inspections = curr_est.record.inspections.all()

        context['masterlist_active'] = "active"
        context['inspections'] = inspections
        return context

class SummaryView(View):
    template_name = 'masterlist/summary.html'

    def get(self, request):
        return render(request, self.template_name)
