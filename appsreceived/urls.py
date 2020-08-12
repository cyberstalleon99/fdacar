from django.urls import path
from .views import ApplicationListView

app_name='appsreceived'

urlpatterns = [
    path('', ApplicationListView.as_view(), name='index'),
]