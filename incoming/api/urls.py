from django.conf.urls import include
from rest_framework import routers
from incoming.api import views
from django.urls import path

app_name='incoming'

router = routers.DefaultRouter()
router.register('all', views.IncomingViewSet)


urlpatterns = [
    path('', include(router.urls)),
]