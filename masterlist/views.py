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
from dashboard.dashboard  import MasterlistSummary
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import MasterlistFilterForm, AddressForm, ExpiredlistFilterForm

class AllListView(LoginRequiredMixin, ListView):
    model = Establishment
    template_name = 'masterlist/index.html'
    context_object_name = 'establishments'

    def get_queryset(self, *args, **kwargs):

        filter = {}

        for field in self.request.GET:
            if field != 'csrfmiddlewaretoken':
                if self.request.GET.get(field) != '':
                    if field == 'region' or field == 'province' or field == 'municipality_or_city':
                        filter['plant_address__' + field] = self.request.GET.get(field)
                    else:
                        filter[field] = self.request.GET.get(field)

        # First load of masterlist page or if filters are empty
        if len(filter) < 1:
            return
        
        qs = Establishment.objects.filter(**filter)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['alllist_active'] = "active"
        context['filter_form'] = MasterlistFilterForm(self.request.GET)
        context['address_form'] = AddressForm(self.request.GET)
        return context

class ExpiredListView(LoginRequiredMixin, ListView):
    model = Establishment
    template_name = 'masterlist/expired-list.html'
    context_object_name = 'establishments'

    def get_queryset(self, *args, **kwargs):
        filter = {}

        for field in self.request.GET:
            if field != 'csrfmiddlewaretoken':
                if self.request.GET.get(field) != '':
                    if field == 'region' or field == 'province' or field == 'municipality_or_city':
                        filter['plant_address__' + field] = self.request.GET.get(field)
                    else:
                        filter[field] = self.request.GET.get(field)

        # First load of masterlist page or if filters are empty
        if len(filter) < 1:
            return

        except_activities = ['Hospital Pharmacy', 'Medical X-Ray', 'Veterinary X-Ray', 'Dental X-Ray', 'Educational X-Ray', 'MRI', 'CTScan', 'Mobile X-Ray']
        qs = Establishment.expiredlist.get_list().exclude(specific_activity__name__in=except_activities).order_by('name')
        qs = qs.filter(**filter)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expiredlist_active'] = "active"
        context['filter_form'] = ExpiredlistFilterForm(self.request.GET)
        context['address_form'] = AddressForm(self.request.GET)
        return context

class AbraListView(LoginRequiredMixin, ListView):
    model = Establishment
    template_name = 'masterlist/abra-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['abra_list_active'] = "active"
        context['provincelist_active'] = "active"
        return context

class ApayaoListView(LoginRequiredMixin, ListView):
    model = Establishment
    template_name = 'masterlist/apayao-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['apayao_list_active'] = "active"
        context['provincelist_active'] = "active"
        return context

class BaguioListView(LoginRequiredMixin, ListView):
    model = Establishment
    template_name = 'masterlist/baguio-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['baguio_list_active'] = "active"
        context['provincelist_active'] = "active"
        return context

class BenguetListView(LoginRequiredMixin, ListView):
    model = Establishment
    template_name = 'masterlist/benguet-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['benguet_list_active'] = "active"
        context['provincelist_active'] = "active"
        return context

class IfugaoListView(LoginRequiredMixin, ListView):
    model = Establishment
    template_name = 'masterlist/ifugao-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['ifugao_list_active'] = "active"
        context['provincelist_active'] = "active"
        return context

class KalingaListView(LoginRequiredMixin, ListView):
    model = Establishment
    template_name = 'masterlist/kalinga-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['kalinga_list_active'] = "active"
        context['provincelist_active'] = "active"
        return context

class MountainListView(LoginRequiredMixin, ListView):
    model = Establishment
    template_name = 'masterlist/mountain-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['mountain_list_active'] = "active"
        context['provincelist_active'] = "active"
        return context



def export_expired(request):
    checklist = Establishment.expiredlist.get_list()
    query = request.GET.get('q', None)
    if query:
        checklist = Establishment.expiredlist.get_filtered_list(query=query)

    response = MyExporter.export_to_xslx(resource=EstablishmentResource(), filename="Expired List Pullout as of {}".format(timezone.now().date()),
    queryset=checklist)
    return response

class EstablishmentDetailView(LoginRequiredMixin, DetailView):
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

        context['qualified_persons'] = curr_est.qualifiedperson_set.filter(status='Active')
        context['masterlist_active'] = "active"
        context['inspections'] = inspections
        return context

class SummaryView(LoginRequiredMixin, View):
    template_name = 'masterlist/summary/summary.html'

    def get(self, request):
        context = {}
        province_obj = MasterlistSummary.Provinces()
        province_list = [attr for attr in dir(province_obj) if not callable(getattr(province_obj, attr)) and not attr.startswith("__")]
        provinces = {}
        for province in province_list:
            provinces[province] = getattr(province_obj, province)

        context['provinces'] = provinces
        context['summary_active'] = "active"

        provinces_data = {}
        for name, prov in provinces.items():
            provinces_data[name] = [prov.cfrr().get_total(), prov.cdrr().get_total(), prov.ccrr().get_total(), prov.cdrrhr().get_total()]
            # print([province.cfrr().get_total(), province.cdrr().get_total(), province.ccrr().get_total(), province.cdrrhr().get_total()])

        print(type(provinces))
        context['provinces_data'] = provinces_data
        context['chart_labels'] = ['Food', 'Drug', 'Cosmetics', 'Medical Device']
        return render(request, self.template_name, context)
