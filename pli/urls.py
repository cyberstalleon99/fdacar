from django.urls import path
from .views import PLIChekListView

app_name='pli'
urlpatterns = [
    path('', PLIChekListView.as_view(), name='index')
]
