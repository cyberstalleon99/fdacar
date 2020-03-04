from django.views.generic import (
    ListView,
    CreateView
)
from django.views.generic.edit import FormView
from .models import Establishment, Lto, ProductType, PrimaryActivity, SpecificActivity, AdditionalActivity, ProductLine, \
    PlantAddress, WarehouseAddress, OfficeAddress, \
    Region, Province, CityOrMunicipality
from .forms import StepOneForm, StepThreeAForm, StepThreeBForm, StepThreeCForm
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
import logging

class MasterListView(ListView):
    template_name = 'masterlist/index.html'
    context_object_name = 'est_list'

    def get_queryset(self):
        return Establishment.objects.all()

class StepOneView(FormView):
    template_name = 'masterlist/stepone.html'
    form_class = StepOneForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
        issuance_val = self.request.POST['issuance']
        lto_number_val = self.request.POST['lto_number']
        expiry_val = self.request.POST['expiry']
        newlto = Lto(issuance=issuance_val, lto_number=lto_number_val, expiry=expiry_val)
        newlto.save()

        application_val = self.request.POST['application']
        name_of_est_val = self.request.POST['name']
        product_type_val = ProductType.objects.get(pk=self.request.POST['product_type'])
        primary_activity_val = PrimaryActivity.objects.get(pk=self.request.POST['primary_activity'])
        product_lines = form.cleaned_data.get('product_line')
        specific_activities = form.cleaned_data.get('specific_activity')
        new_est = Establishment.objects.create(application=application_val, name=name_of_est_val, lto=newlto, product_type=product_type_val, primary_activity=primary_activity_val, center='Test')
        new_est.specific_activity.set(specific_activities)
        new_est.product_line.set(product_lines)
        new_est.save()
        self.request.session['est_id'] = new_est.id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('masterlist:stepthree-a')

class StepThreeAView(FormView):
    # model = PlantAddress
    form_class = StepThreeAForm
    template_name = 'masterlist/steptwo-a.html'

    def form_valid(self, form):
        est_id = self.request.session['est_id']
        curr_est = Establishment.objects.get(pk=est_id)
        curr_est.plant_address = PlantAddress(address=self.request.POST['address'],
                                              region=Region.objects.get(pk=self.request.POST['region']),
                                              province=Province.objects.get(pk=self.request.POST['province']),
                                              municipality_or_city=CityOrMunicipality.objects.get(pk=self.request.POST['municipality_or_city'])).save()
        curr_est.save()
        return super().form_valid(form)

    # Redirect to Tool List after successful registration
    def get_success_url(self):
        return reverse('masterlist:stepthree-b')

class StepThreeBView(CreateView):
    model = WarehouseAddress
    form_class = StepThreeBForm
    template_name = 'masterlist/steptwo-b.html'
    # success_url = reverse_lazy('masterlist:stepthree-c')

    def form_valid(self, form):
        return super().form_valid(form)

    # Redirect to Tool List after successful registration
    def get_success_url(self):
        return reverse('masterlist:stepthree-c')

class StepThreeCView(CreateView):
    model = OfficeAddress
    form_class = StepThreeBForm
    template_name = 'masterlist/steptwo-c.html'
    success_url = reverse_lazy('masterlist:stepthree-c')

def load_provinces(request):
    region_id = request.GET.get('region')
    provinces = Province.objects.filter(region_id=region_id).order_by('name')
    return render(request, 'masterlist/province_dropdown_list_options.html', {'provinces': provinces})

def load_cities(request):
    province_id = request.GET.get('province')
    cities_or_municipalities = CityOrMunicipality.objects.filter(province_id=province_id).order_by('name')
    return render(request, 'masterlist/municipality_dropdown_list_options.html', {'cities_or_municipalities':cities_or_municipalities})

def load_productlines(request):
    product_type_id = request.GET.get('productType')
    product_lines = ProductLine.objects.filter(product_type_id=product_type_id).order_by('name')
    return render(request, 'masterlist/productline_dropdown_list_options.html', {'product_lines': product_lines})
