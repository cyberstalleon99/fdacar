from rest_framework import viewsets
from .serializers import IncomingSerializer
from incoming.models import Incoming

class IncomingViewSet(viewsets.ModelViewSet):
    queryset = Incoming.objects.all().order_by('date_received')
    serializer_class = IncomingSerializer