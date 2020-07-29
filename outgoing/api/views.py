from rest_framework import viewsets
from .serializers import OutgoingSerializer
from outgoing.models import Outgoing

class OutgoingViewSet(viewsets.ModelViewSet):
    queryset = Outgoing.objects.all().order_by('group')
    serializer_class = OutgoingSerializer