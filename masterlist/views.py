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
from .forms import StepOneForm, StepTwoAForm, StepTwoBForm, StepTwoCForm, StepThreeForm
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q
from . import mypaginator

class EstablishmentListView(ListView):
    model = Establishment
    items_per_page = 10
    template_name = 'masterlist/index.html'
    context_object_name = 'test'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['masterlist_active'] = "active"
        page = self.request.GET.get('page')
        paginator = mypaginator.MyPaginator(self.get_establishments(), self.items_per_page, page)
        establishments = paginator.get_paginated_result()
        context['paginated_result'] = establishments
        return context

    # TODO: Add additional filters
    def get_establishments(self):
        establishments = Establishment.objects.all()
        query = self.request.GET.get('q', None)
        if query is not None:
            establishments = Establishment.objects.filter(
                Q(name__icontains=query) |
                Q(center__icontains=query)
            )
        return establishments

class EstablishmentDetailView(DetailView):
    template_name = 'masterlist/establishment-detail.html'
    context_object_name = 'establishment'

    def get_object(self):
        est_id =self.kwargs.get("id")
        return get_object_or_404(Establishment, id=est_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        curr_est = Establishment.objects.get(pk=self.kwargs.get('id'))
        curr_est.lto.get_duration()
        inspections = curr_est.inspection_set.all()
        context['masterlist_active'] = "active"
        context['inspections'] = inspections
        return context

class ExpiredEstablishmentsListView(ListView):
        model = Establishment
        # items_per_page = 10
        template_name = 'masterlist/expired-list.html'
        context_object_name = 'test'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['expiredlist_active'] = "active"
            context['paginated_result'] = Establishment.objects.filter()

class StepOneView(FormView):
    template_name = 'masterlist/stepone.html'
    form_class = StepOneForm

    # def get(self, request, *args, **kwargs):
    #     form = self.form_class
    #     return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
        issuance_val = self.request.POST['issuance']
        lto_number_val = self.request.POST['lto_number']
        expiry_val = self.request.POST['expiry']

        form = StepOneForm(self.request.POST)
        newform = form.save(commit=False)
        # newform.lto = newlto
        newform.save()
        form.save_m2m()
        self.request.session['est_id'] = newform.id
        est = Establishment.objects.get(pk=newform.id)
        newlto = Lto(establishment=est, issuance=issuance_val, lto_number=lto_number_val, expiry=expiry_val)
        newlto.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('masterlist:steptwo-a')

class StepTwoAView(FormView):
    form_class = StepTwoAForm
    template_name = 'masterlist/steptwo-a.html'

    def form_valid(self, form):
        curr_est = Establishment.objects.get(pk=self.request.session['est_id'])
        curr_est.plant_address = PlantAddress.objects.create(address=self.request.POST['address'],
                                              region=Region.objects.get(pk=self.request.POST['region']),
                                              province=Province.objects.get(pk=self.request.POST['province']),
                                              municipality_or_city=CityOrMunicipality.objects.get(pk=self.request.POST['municipality_or_city']))
        curr_est.save()
        return super().form_valid(form)

    # Redirect to Tool List after successful registration
    def get_success_url(self):
        return reverse('masterlist:steptwo-b')

class StepTwoBView(FormView):
    form_class = StepTwoBForm
    template_name = 'masterlist/steptwo-b.html'

    def form_valid(self, form):
        curr_est = Establishment.objects.get(pk=self.request.session['est_id'])
        curr_est.warehouse_address = WarehouseAddress.objects.create(address=self.request.POST['address'],
                                              region=Region.objects.get(pk=self.request.POST['region']),
                                              province=Province.objects.get(pk=self.request.POST['province']),
                                              municipality_or_city=CityOrMunicipality.objects.get(pk=self.request.POST['municipality_or_city']))
        curr_est.save()
        return super().form_valid(form)

    # Redirect to Tool List after successful registration
    def get_success_url(self):
        return reverse('masterlist:steptwo-c')

class StepTwoCView(FormView):
    form_class = StepTwoCForm
    template_name = 'masterlist/steptwo-c.html'

    def form_valid(self, form):
        curr_est = Establishment.objects.get(pk=self.request.session['est_id'])
        curr_est.office_address = OfficeAddress.objects.create(address=self.request.POST['address'],
                                              region=Region.objects.get(pk=self.request.POST['region']),
                                              province=Province.objects.get(pk=self.request.POST['province']),
                                              municipality_or_city=CityOrMunicipality.objects.get(pk=self.request.POST['municipality_or_city']))
        curr_est.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('masterlist:stepthree')

class StepThreeView(FormView):
    form_class = StepThreeForm
    template_name = 'masterlist/stepthree.html'

    def form_valid(self, form):
        curr_est = Establishment.objects.get(pk=self.request.session['est_id'])
        curr_est.authorized_officer = AuthorizedOfficer.objects.create(first_name=self.request.POST['authorized_firstname'],
                                                                       last_name=self.request.POST['authorized_lastname'],
                                                                       middle_initial=self.request.POST['authorized_middleinit'],
                                                                       designation=AuthorizedOfficerDesignation.objects.get(pk=self.request.POST['authorized_desig']))
        curr_est.status = self.request.POST['status']
        QualifiedPerson(first_name=self.request.POST['qualified_firstname'],
                       last_name=self.request.POST['qualified_lastname'],
                       middle_initial=self.request.POST['qualified_middleinit'],
                       designation=QualifiedPersonDesignation.objects.get(pk=self.request.POST['qualified_desig']), establishment=curr_est).save()
        curr_est.save()
        return super().form_valid(form)

    # Redirect to Tool List after successful registration
    def get_success_url(self):
        return reverse('masterlist:index')


def load_provinces(request):
    region_id = request.GET.get('region')
    provinces = Province.objects.filter(region_id=region_id).order_by('name')
    return render(request, 'masterlist/ajax-templates/province_dropdown_list_options.html', {'provinces': provinces})

def load_cities(request):
    province_id = request.GET.get('province')
    cities_or_municipalities = CityOrMunicipality.objects.filter(province_id=province_id).order_by('name')
    return render(request, 'masterlist/ajax-templates/municipality_dropdown_list_options.html', {'cities_or_municipalities':cities_or_municipalities})

def load_productlines(request):
    product_type_id = request.GET.get('productType')
    product_lines = ProductLine.objects.filter(product_type_id=product_type_id).order_by('name')
    return render(request, 'masterlist/ajax-templates/productline_dropdown_list_options.html', {'product_lines': product_lines})
