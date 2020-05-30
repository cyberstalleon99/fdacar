from django.urls import path
from .views import ( AllListView, EstablishmentDetailView, ExpiredListView, InactiveListView,
                     AbraListView, ApayaoListView, BaguioListView, BenguetListView, IfugaoListView, KalingaListView, MountainListView,
                     SummaryView)
app_name='masterlist'

from masterlist import views

urlpatterns = [
    path('', AllListView.as_view(), name='index'),
    path('all/', AllListView.as_view(), name='index'),

    path('abra/', AbraListView.as_view(), name='abra-list'),
    path('apayao/', ApayaoListView.as_view(), name='apayao-list'),
    path('baguio/', BaguioListView.as_view(), name='baguio-list'),
    path('benguet/', BenguetListView.as_view(), name='benguet-list'),
    path('ifugao/', IfugaoListView.as_view(), name='ifugao-list'),
    path('kalinga/', KalingaListView.as_view(), name='kalinga-list'),
    path('mountain/', MountainListView.as_view(), name='mountain-list'),

    path('expired/', ExpiredListView.as_view(), name='expired-list'),
    path('export-expired/', views.export_expired, name='export-expired'),

    path('inactive/', InactiveListView.as_view(), name='inactive-list'),
    # path('export-inactive/', InactiveListView.export, name='export-inactive'),

    path('summary/', SummaryView.as_view(), name='summary'),

    path('<int:id>/', EstablishmentDetailView.as_view(), name='est-detail'),

]
