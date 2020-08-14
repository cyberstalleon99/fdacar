from django.conf.urls import include
from rest_framework import routers
from masterlist.api import views
from django.urls import path

app_name='masterlist'

router = routers.DefaultRouter()
router.register('all', views.EstablishmentViewSet)
router.register('closed', views.ClosedViewSet)
router.register('inactive', views.InactiveViewSet)
router.register('abra', views.AbraViewSet)
router.register('apayao', views.ApayaoViewSet)
router.register('baguio', views.BaguioViewSet)
router.register('benguet', views.BenguetViewSet)
router.register('ifugao', views.IfugaoViewSet)
router.register('kalinga', views.KalingaViewSet)
router.register('mountain', views.MountainViewSet)
router.register('expired', views.ExpiredViewSet)

urlpatterns = [
    path('', include(router.urls)),
]