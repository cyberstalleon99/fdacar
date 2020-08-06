from django.urls import path
from .views import PmsListView

app_name='pms'

urlpatterns = [
    path('', PmsListView.as_view(), name='index'),

]
