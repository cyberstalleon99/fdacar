from django.contrib import admin
from .models import Job

# admin.site.register(Job)

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    model = Job
    list_per_page = 20

    list_display = ('name', 'inspection_type', 'inspection_status')

    def name(self, obj):
        return obj.establishment.name
