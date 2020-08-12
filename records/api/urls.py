from django.conf.urls import include
from rest_framework import routers
from appsreceived.api import views
from django.urls import path

app_name='appsreceived'

router = routers.DefaultRouter()
router.register('all', views.ApplicationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]