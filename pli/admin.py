from django.contrib import admin
from .models import Pli, PliStatus

admin.site.register(PliStatus)
admin.site.register(Pli)