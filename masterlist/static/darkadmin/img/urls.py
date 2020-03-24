from django.urls import path
from .views import EstablishmentSummaryView
from . import views

app_name='listsummary'
urlpatterns = [
    path('', EstablishmentSummaryView.as_view(), name='summary'),
]
