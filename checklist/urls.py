from django.urls import path
from .views import RenewalChekListView, PliChekListView, RoutineChekListView
from . import views

app_name='checklist'
urlpatterns = [
    path('', RenewalChekListView.as_view(), name='index'),
    path('export-renewal/', views.export_renewal, name='export-renewal'),

    path('pli/', PliChekListView.as_view(), name='pli'),
    path('export-pli/', views.export_pli, name='export-pli'),

    path('routine/', RoutineChekListView.as_view(), name='routine'),
    path('export-routine/', views.export_routine, name='export-routine'),
]
