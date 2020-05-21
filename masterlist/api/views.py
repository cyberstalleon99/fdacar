from django.shortcuts import render
from rest_framework import viewsets
from .serializers import EstablishmentSerializer
from masterlist.models import Establishment

def index(request):
    return render (request, 'masterlist/index.html')

class EstablishmentViewSet(viewsets.ModelViewSet):
    queryset = Establishment.objects.all().order_by('name')
    serializer_class = EstablishmentSerializer
    # context={'request': request}