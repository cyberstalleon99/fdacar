from rest_framework import viewsets
from .serializers import RenewalSerializer
from checklist.models import Job

class RenewalViewSet(viewsets.ModelViewSet):
    queryset = Job.renchecklist.get_list().order_by('establishment__ltos__expiry')
    serializer_class = RenewalSerializer

class PLIViewSet(viewsets.ModelViewSet):
    queryset = Job.plichecklist.get_list().order_by('name')
    serializer_class = RenewalSerializer
