from django.urls import path
# from .views import ( AllListView, EstablishmentDetailView, ExpiredListView, ClosedListView,
#                      AbraListView, ApayaoListView, BaguioListView, BenguetListView, IfugaoListView, KalingaListView, MountainListView,
#                      SummaryView, InactiveListView)
from .views import create_folder_view
app_name='records'


# from masterlist import views

urlpatterns = [
    path('create/', create_folder_view, name='record-add'),
]
