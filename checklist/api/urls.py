from django.conf.urls import include
from rest_framework import routers
from checklist.api import views
from django.urls import path

app_name='checklist'

router = routers.DefaultRouter()
router.register('ren', views.RenewalViewSet)
router.register('pli', views.PLIViewSet)
# router.register('abra', views.AbraViewSet)

urlpatterns = [
    path('', include(router.urls)),
]