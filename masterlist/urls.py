from django.urls import path
from .views import ( AllListView, FoodListView, DrugListView, CosmeticListView, MedicalDeviceListView,
                     # StepOneView, StepTwoAView, StepTwoBView, StepTwoCView, StepThreeView,
                     EstablishmentDetailView, ExpiredListView, InactiveListView)
from . import views

app_name='masterlist'
urlpatterns = [
    path('', AllListView.as_view(), name='index'),
    path('all/', AllListView.as_view(), name='index'),
    path('export-all/', AllListView.export, name='export-all'),

    path('food/', FoodListView.as_view(), name='food-list'),
    path('export-food/', FoodListView.export, name='export-food'),

    path('drug/', DrugListView.as_view(), name='drug-list'),
    path('export-drug/', DrugListView.export, name='export-drug'),

    path('cosmetic/', CosmeticListView.as_view(), name='cosmetic-list'),
    path('export-cosmetic/', CosmeticListView.export, name='export-cosmetic'),

    path('medical-device/', MedicalDeviceListView.as_view(), name='medicaldevice-list'),
    path('export-medicaldevice/', MedicalDeviceListView.export, name='export-medicaldevice'),

    path('expired/', ExpiredListView.as_view(), name='expired-list'),
    path('export-expired/', views.export_expired, name='export-expired'),

    path('inactive/', InactiveListView.as_view(), name='inactive-list'),
    path('export-inactive/', InactiveListView.export, name='export-inactive'),

    path('<int:id>/', EstablishmentDetailView.as_view(), name='est-detail'),


]
