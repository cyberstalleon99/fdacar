from django.contrib import admin
from .models import Incoming, DocumentType

admin.site.register(Incoming)
admin.site.register(DocumentType)
