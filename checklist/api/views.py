from rest_framework import viewsets
from .serializers import RenewalSerializer
from checklist.models import Job

class RenewalViewSet(viewsets.ModelViewSet):
    queryset = Job.renchecklist.get_list().filter(establishment__status='Active').order_by('name')
    serializer_class = RenewalSerializer

class PLIViewSet(viewsets.ModelViewSet):
    queryset = Job.plichecklist.get_list().filter(establishment__status='Active').order_by('name')
    serializer_class = RenewalSerializer