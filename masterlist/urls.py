from django.urls import path
from .views import ( AllListView, FoodListView, DrugListView, CosmeticListView, MedicalDeviceListView,
                     StepOneView, StepTwoAView, StepTwoBView, StepTwoCView, StepThreeView,
                     EstablishmentDetailView, ExpiredListView )
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

    path('<int:id>/', EstablishmentDetailView.as_view(), name='est-detail'),

    path('add-stepone/', StepOneView.as_view(), name='stepone'),
    path('add-steptwo-a/', StepTwoAView.as_view(), name='steptwo-a'),
    path('add-steptwo-b/', StepTwoBView.as_view(), name='steptwo-b'),
    path('add-steptwo-c/', StepTwoCView.as_view(), name='steptwo-c'),
    path('add-stepthree/', StepThreeView.as_view(), name='stepthree'),
    path('load-provinces/', views.load_provinces, name='ajax_load_provinces'),
    path('load-cities/', views.load_cities, name='ajax_load_cities'),
    path('load-productlines/', views.load_productlines, name='ajax_load_productlines'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # path('<int:pk>/results/', views.ResultView.as_view(), name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]
