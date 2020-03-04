from django.urls import path
from .views import EstablishmentListView, StepOneView, StepTwoAView, StepTwoBView, StepTwoCView, StepThreeView, EstablishmentDetailView
from . import views

app_name='masterlist'
urlpatterns = [
    path('', EstablishmentListView.as_view(), name='index'),
    path('<int:id>/', EstablishmentDetailView.as_view(), name='est-detail'),

    path('add-stepone/', StepOneView.as_view(), name='stepone'),
    path('add-steptwo-a/', StepTwoAView.as_view(), name='steptwo-a'),
    path('add-steptwo-b/', StepTwoBView.as_view(), name='steptwo-b'),
    path('add-steptwo-c/', StepTwoCView.as_view(), name='steptwo-c'),
    path('add-stepthree/', StepThreeView.as_view(), name='stepthree'),
    path('load-provinces/', views.load_provinces, name='ajax_load_provinces'),
    path('load-cities/', views.load_cities, name='ajax_load_cities'),
    path('load-productlines/', views.load_productlines, name='ajax_load_productlines'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # path('<int:pk>/results/', views.ResultView.as_view(), name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]