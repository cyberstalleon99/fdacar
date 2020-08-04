from django.conf.urls import include
from rest_framework import routers
from pli.api import views
from django.urls import path

app_name='pli'

router = routers.DefaultRouter()
router.register('all', views.PliViewSet)

urlpatterns = [
    path('', include(router.urls)),
]