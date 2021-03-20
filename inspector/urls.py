from django.urls import path
from .views import InspectorProfileView

app_name='inspector'

urlpatterns = [
    path('<int:id>/', InspectorProfileView.as_view(), name='index'),
]
