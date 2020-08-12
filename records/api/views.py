from rest_framework import viewsets
from .serializers import AppsReceivedSerializer
from appsreceived.models import Application

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all().order_by('group')
    serializer_class = AppsReceivedSerializer