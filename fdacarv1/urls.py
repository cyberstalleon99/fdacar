
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('masterlist/', include('masterlist.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('checklist/', include('checklist.urls')),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),

    # API URLS
    path('api/est-list/', include('masterlist.api.urls', 'masterlist-api')),
    path('api/checklist/', include('checklist.api.urls', 'checklist-api')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
