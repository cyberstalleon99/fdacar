from rest_framework import viewsets
from .serializers import PliSerializer
from pli.models import Pli

class PliViewSet(viewsets.ModelViewSet):
    queryset = Pli.objects.all()
    serializer_class = PliSerializer