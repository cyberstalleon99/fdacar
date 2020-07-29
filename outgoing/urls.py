from django.urls import path
from .views import OutgoingListView

app_name='outgoing'

urlpatterns = [
    path('', OutgoingListView.as_view(), name='index'),

]
