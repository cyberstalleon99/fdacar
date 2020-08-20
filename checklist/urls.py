from django.urls import path
from .views import RenewalChekListView, PliChekListView, RoutineChekListView

app_name='checklist'
urlpatterns = [
    path('', RenewalChekListView.as_view(), name='index'),
    path('pli/', PliChekListView.as_view(), name='pli'),
    path('routine/', RoutineChekListView.as_view(), name='routine'),
]
