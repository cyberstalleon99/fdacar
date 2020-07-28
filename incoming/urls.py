from django.urls import path
from .views import IncomingListView

app_name='incoming'
urlpatterns = [
    path('', IncomingListView.as_view(), name='index'),

]
