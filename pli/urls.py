from django.urls import path
from .views import PliListView

app_name='pli'

urlpatterns = [
    path('', PliListView.as_view(), name='index'),

]
