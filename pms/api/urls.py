from django.conf.urls import include
from rest_framework import routers
from pms.api import views
from django.urls import path

app_name='pms'

router = routers.DefaultRouter()
router.register('all', views.ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]