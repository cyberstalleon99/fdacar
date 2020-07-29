from django.conf.urls import include
from rest_framework import routers
from outgoing.api import views
from django.urls import path

app_name='outgoing'

router = routers.DefaultRouter()
router.register('all', views.OutgoingViewSet)


urlpatterns = [
    path('', include(router.urls)),
]