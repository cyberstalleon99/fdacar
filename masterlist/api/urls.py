from django.conf.urls import include
from rest_framework import routers
from masterlist.api import views
from django.urls import path

app_name='masterlist'

router = routers.DefaultRouter()
router.register('estabs', views.EstablishmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]