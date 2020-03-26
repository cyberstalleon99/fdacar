from django.urls import path
from .views import RenewalChekListView, PliChekListView

app_name='checklist'
urlpatterns = [
    path('', RenewalChekListView.as_view(), name='index'),
    path('pli/', PliChekListView.as_view(), name='pli'),
]
