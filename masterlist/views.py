from django.views.generic import (
    ListView,
    CreateView,
    DetailView
)
from django.views import View
from django.views.generic.edit import FormView
from .models import Establishment, Lto, ProductType, PrimaryActivity, SpecificActivity, AdditionalActivity, ProductLine, \
    PlantAddress, WarehouseAddress, OfficeAddress, \
    Region, Province, CityOrMunicipality, AuthorizedOfficer, AuthorizedOfficerDesignation, QualifiedPerson, QualifiedPersonDesignation
# from .forms import StepOneForm, StepTwoAForm, StepTwoBForm, StepTwoCForm, StepThreeForm
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.db.models import Q
from . import mypaginator
from .masterlistview import MasterListView
from .myhelpers import MyExporter
from .myresources import EstablishmentResource

class AllListView(MasterListView):
    template_name = 'masterlist/index.html'

    def get_context_data(self, **kwargs):
        establishments = Establishment.objects.all()
        super().init_establishments(establishments)
        context = super().get_context_data()
        context['alllist_active'] = "active"
        return context

    def export(self):
        response = MyExporter.export_to_xslx(resource=EstablishmentResource(), filename="Masterlist Pullout as of {}".format(timezone.now().date()),
        queryset=Establishment.objects.all())
        return response

class FoodListView(MasterListView):
    template_name = 'masterlist/food-list.html'

    def get_context_data(self, **kwargs):
        establishments = Establishment.objects.filter(product_type__name='Food')
        super().init_establishments(establishments)
        context = super().get_context_data()
        context['foodlist_active'] = "active"
        return context

    def export(self):
        response = MyExporter.export_to_xslx(resource=EstablishmentResource(), filename="Food List Pullout as of {}".format(timezone.now().date()),
        queryset=Establishment.objects.filter(product_type__name='Food'))
        return response

class DrugListView(MasterListView):
    template_name = 'masterlist/drug-list.html'

    def get_context_data(self, **kwargs):
        establishments = Establishment.objects.filter(product_type__name='Drug')
        super().init_establishments(establishments)
        context = super().get_context_data()
        context['druglist_active'] = "active"
        return context

    def export(self):
        response = MyExporter.export_to_xslx(resource=EstablishmentResource(), filename="Drug List Pullout as of {}".format(timezone.now().date()),
        queryset=Establishment.objects.filter(product_type__name='Drug'))
        return response

class CosmeticListView(MasterListView):
    template_name = 'masterlist/cosmetic-list.html'

    def get_context_data(self, **kwargs):
        establishments = Establishment.objects.filter(product_type__name='Cosmetic')
        super().init_establishments(establishments)
        context = super().get_context_data()
        context['cosmeticlist_active'] = "active"
        return context

    def export(self):
        response = MyExporter.export_to_xslx(resource=EstablishmentResource(), filename="Cosmetic List Pullout as of {}".format(timezone.now().date()),
        queryset=Establishment.objects.filter(product_type__name='Cosmetic'))
        return response

class MedicalDeviceListView(MasterListView):
    template_name = 'masterlist/medicaldevice-list.html'

    def get_context_data(self, **kwargs):
        establishments = Establishment.objects.filter(product_type__name='Medical Device')
        super().init_establishments(establishments)
        context = super().get_context_data()
        context['medicaldevice_active'] = "active"
        return context

    def export(self):
        response = MyExporter.export_to_xslx(resource=EstablishmentResource(), filename="MedicalDevices List Pullout as of {}".format(timezone.now().date()),
        queryset=Establishment.objects.filter(product_type__name='Medical Device'))
        return response

class ExpiredListView(ListView):
    model = Establishment
    items_per_page = 10
    template_name = 'masterlist/expired-list.html'
    context_object_name = 'test'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expiredlist_active'] = "active"
        page = self.request.GET.get('page')
        paginator = mypaginator.MyPaginator(self.get_list(), self.items_per_page, page)
        establishments = paginator.get_paginated_result()
        context['paginated_result'] = establishments
        context['result_count'] = paginator.get_result_count()
        return context

    def get_list(self):
        checklist = Establishment.expiredlist.get_list()
        query = self.request.GET.get('q', None)
        if query:
            checklist = Establishment.expiredlist.get_filtered_list(query=query)
        return checklist

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
        inspections = curr_est.record.inspection_set.all()
        context['masterlist_active'] = "active"
        context['inspections'] = inspections
        return context

# class StepOneView(FormView):
#     template_name = 'masterlist/stepone.html'
#     form_class = StepOneForm
#
#     # def get(self, request, *args, **kwargs):
#     #     form = self.form_class
#     #     return render(request, self.template_name, {'form': form})
#
#     def form_valid(self, form):
#         issuance_val = self.request.POST['issuance']
#         lto_number_val = self.request.POST['lto_number']
#         expiry_val = self.request.POST['expiry']
#
#         form = StepOneForm(self.request.POST)
#         newform = form.save(commit=False)
#         # newform.lto = newlto
#         newform.save()
#         form.save_m2m()
#         self.request.session['est_id'] = newform.id
#         est = Establishment.objects.get(pk=newform.id)
#         newlto = Lto(establishment=est, issuance=issuance_val, lto_number=lto_number_val, expiry=expiry_val)
#         newlto.save()
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return reverse('masterlist:steptwo-a')
#
# class StepTwoAView(FormView):
#     form_class = StepTwoAForm
#     template_name = 'masterlist/steptwo-a.html'
#
#     def form_valid(self, form):
#         curr_est = Establishment.objects.get(pk=self.request.session['est_id'])
#         curr_est.plant_address = PlantAddress.objects.create(address=self.request.POST['address'],
#                                               region=Region.objects.get(pk=self.request.POST['region']),
#                                               province=Province.objects.get(pk=self.request.POST['province']),
#                                               municipality_or_city=CityOrMunicipality.objects.get(pk=self.request.POST['municipality_or_city']))
#         curr_est.save()
#         return super().form_valid(form)
#
#     # Redirect to Tool List after successful registration
#     def get_success_url(self):
#         return reverse('masterlist:steptwo-b')
#
# class StepTwoBView(FormView):
#     form_class = StepTwoBForm
#     template_name = 'masterlist/steptwo-b.html'
#
#     def form_valid(self, form):
#         curr_est = Establishment.objects.get(pk=self.request.session['est_id'])
#         curr_est.warehouse_address = WarehouseAddress.objects.create(address=self.request.POST['address'],
#                                               region=Region.objects.get(pk=self.request.POST['region']),
#                                               province=Province.objects.get(pk=self.request.POST['province']),
#                                               municipality_or_city=CityOrMunicipality.objects.get(pk=self.request.POST['municipality_or_city']))
#         curr_est.save()
#         return super().form_valid(form)
#
#     # Redirect to Tool List after successful registration
#     def get_success_url(self):
#         return reverse('masterlist:steptwo-c')
#
# class StepTwoCView(FormView):
#     form_class = StepTwoCForm
#     template_name = 'masterlist/steptwo-c.html'
#
#     def form_valid(self, form):
#         curr_est = Establishment.objects.get(pk=self.request.session['est_id'])
#         curr_est.office_address = OfficeAddress.objects.create(address=self.request.POST['address'],
#                                               region=Region.objects.get(pk=self.request.POST['region']),
#                                               province=Province.objects.get(pk=self.request.POST['province']),
#                                               municipality_or_city=CityOrMunicipality.objects.get(pk=self.request.POST['municipality_or_city']))
#         curr_est.save()
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return reverse('masterlist:stepthree')
#
# class StepThreeView(FormView):
#     form_class = StepThreeForm
#     template_name = 'masterlist/stepthree.html'
#
#     def form_valid(self, form):
#         curr_est = Establishment.objects.get(pk=self.request.session['est_id'])
#         curr_est.authorized_officer = AuthorizedOfficer.objects.create(first_name=self.request.POST['authorized_firstname'],
#                                                                        last_name=self.request.POST['authorized_lastname'],
#                                                                        middle_initial=self.request.POST['authorized_middleinit'],
#                                                                        designation=AuthorizedOfficerDesignation.objects.get(pk=self.request.POST['authorized_desig']))
#         curr_est.status = self.request.POST['status']
#         QualifiedPerson(first_name=self.request.POST['qualified_firstname'],
#                        last_name=self.request.POST['qualified_lastname'],
#                        middle_initial=self.request.POST['qualified_middleinit'],
#                        designation=QualifiedPersonDesignation.objects.get(pk=self.request.POST['qualified_desig']), establishment=curr_est).save()
#         curr_est.save()
#         return super().form_valid(form)
#
#     # Redirect to Tool List after successful registration
#     def get_success_url(self):
#         return reverse('masterlist:index')
#
#
# def load_provinces(request):
#     region_id = request.GET.get('region')
#     provinces = Province.objects.filter(region_id=region_id).order_by('name')
#     return render(request, 'masterlist/ajax-templates/province_dropdown_list_options.html', {'provinces': provinces})
#
# def load_cities(request):
#     province_id = request.GET.get('province')
#     cities_or_municipalities = CityOrMunicipality.objects.filter(province_id=province_id).order_by('name')
#     return render(request, 'masterlist/ajax-templates/municipality_dropdown_list_options.html', {'cities_or_municipalities':cities_or_municipalities})
#
# def load_productlines(request):
#     product_type_id = request.GET.get('productType')
#     product_lines = ProductLine.objects.filter(product_type_id=product_type_id).order_by('name')
#     return render(request, 'masterlist/ajax-templates/productline_dropdown_list_options.html', {'product_lines': product_lines})
