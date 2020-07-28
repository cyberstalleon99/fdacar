from django.contrib import admin
from .models import Outgoing, Courier

admin.site.register(Courier)
admin.site.register(Outgoing)
