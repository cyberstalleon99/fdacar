from rest_framework import viewsets
from .serializers import EstablishmentSerializer
from masterlist.models import Establishment

class EstablishmentViewSet(viewsets.ModelViewSet):
    queryset = Establishment.objects.filter(status='Active').order_by('date_modified')[:5]
    serializer_class = EstablishmentSerializer

class ClosedViewSet(viewsets.ModelViewSet):
    queryset = Establishment.objects.filter(status='Closed').order_by('name')
    serializer_class = EstablishmentSerializer

class InactiveViewSet(viewsets.ModelViewSet):
    queryset = Establishment.objects.filter(status='Inactive').order_by('name')
    serializer_class = EstablishmentSerializer

class AbraViewSet(viewsets.ModelViewSet):
    queryset = Establishment.objects.filter(status='Active', plant_address__province__name='Abra').order_by('name')
    serializer_class = EstablishmentSerializer

class ApayaoViewSet(viewsets.ModelViewSet):
    queryset = Establishment.objects.filter(status='Active', plant_address__province__name='Apayao').order_by('name')
    serializer_class = EstablishmentSerializer

class BaguioViewSet(viewsets.ModelViewSet):
    queryset = Establishment.objects.filter(status='Active', plant_address__municipality_or_city__name='Baguio City').order_by('name')
    serializer_class = EstablishmentSerializer

class BenguetViewSet(viewsets.ModelViewSet):
    queryset = Establishment.objects.filter(status='Active', plant_address__province__name='Benguet').exclude(plant_address__municipality_or_city__name='Baguio City').order_by('name')
    serializer_class = EstablishmentSerializer

class IfugaoViewSet(viewsets.ModelViewSet):
    queryset = Establishment.objects.filter(status='Active', plant_address__province__name='Ifugao').order_by('name')
    serializer_class = EstablishmentSerializer

class KalingaViewSet(viewsets.ModelViewSet):
    queryset = Establishment.objects.filter(status='Active', plant_address__province__name='Kalinga').order_by('name')
    serializer_class = EstablishmentSerializer

class MountainViewSet(viewsets.ModelViewSet):
    queryset = Establishment.objects.filter(status='Active', plant_address__province__name='Mountain Province').order_by('name')
    serializer_class = EstablishmentSerializer

class ExpiredViewSet(viewsets.ModelViewSet):
    except_activities = ['Hospital Pharmacy', 'Medical X-Ray', 'Veterinary X-Ray', 'Dental X-Ray', 'Educational X-Ray', 'MRI', 'CTScan', 'Mobile X-Ray']
    queryset = Establishment.expiredlist.get_list().exclude(specific_activity__name__in=except_activities).order_by('name')
    serializer_class = EstablishmentSerializer