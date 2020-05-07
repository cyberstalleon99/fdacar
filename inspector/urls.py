from django.urls import path
from .views import DashboardView
from . import views

app_name='inspector'
urlpatterns = [
    # path('', DashboardView.as_view(), name='index'),
]
