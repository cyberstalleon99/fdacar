
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('masterlist/', include('masterlist.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('checklist/', include('checklist.urls')),
    path('accounts/', include('accounts.urls')),
    path('incoming/', include('incoming.urls')),
    path('outgoing/', include('outgoing.urls')),
    path('pli/', include('pli.urls')),
    path('pms/', include('pms.urls')),
    path('appsreceived/', include('appsreceived.urls')),
    path('records/', include('records.urls')),
    path('profile/', include('inspector.urls')),

    # API URLS
    path('api/est-list/', include('masterlist.api.urls', 'masterlist-api')),
    path('api/checklist/', include('checklist.api.urls', 'checklist-api')),
    path('api/incoming/', include('incoming.api.urls', 'incoming-api')),
    path('api/outgoing/', include('outgoing.api.urls', 'outgoing-api')),
    path('api/pli/', include('pli.api.urls', 'pli-api')),
    path('api/pms/', include('pms.api.urls', 'pms-api')),
    path('api/appsreceived/', include('appsreceived.api.urls', 'appsreceived-api')),

    # Dependent Dropdown URL
    url(r'^chaining/', include('smart_selects.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
