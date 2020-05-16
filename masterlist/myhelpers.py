from django.db.models import Q
from django.db import models
from django.http import HttpResponse


class MyModelManager(models.Manager):

    def check_for_inspection(self):
        pass

    def get_filtered_list(self, query):
        self.check_for_inspection()
        jobs = self.get_list().filter(
            Q(establishment__name__icontains=query) |
            Q(establishment__plant_address__address__icontains=query) |
            Q(establishment__plant_address__municipality_or_city__name__icontains=query) |
            Q(establishment__plant_address__region__name__icontains=query) |
            Q(establishment__plant_address__province__name__icontains=query) |
            Q(establishment__product_type__name__icontains=query) |
            Q(establishment__primary_activity__name__icontains=query) |
            Q(establishment__specific_activity__name__icontains=query) |
            Q(establishment__ltos__lto_number__icontains=query)
        ).distinct()
        return jobs

    def get_list(self):
        pass

    def get(self, establishments):
        pass

class MyExporter:

    # TODO: Add other export types refer to this link: https://simpleisbetterthancomplex.com/packages/2016/08/11/django-import-export.html
    def export_to_xslx(resource, filename, queryset):
        dataset = resource.export(queryset)
        response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename={}.xlsx'.format(filename)
        return response
