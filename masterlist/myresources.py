from import_export import resources, fields
from .models import Establishment, SpecificActivity, Lto
from import_export.widgets import ManyToManyWidget, ForeignKeyWidget

class EstablishmentResource(resources.ModelResource):
    specific_activities = fields.Field(column_name="Specific Activity/s")
    lto = fields.Field(column_name="LTO Number")
    lto_expiry = fields.Field(column_name="Expiry")

    def dehydrate_specific_activities(self, establishment):
        specific_activities = ''
        for spec_act in establishment.specific_activity.all():
            specific_activities += spec_act.name + ", "
        return specific_activities

    def dehydrate_lto(self, establishment):
        return establishment.ltos.latest()

    def dehydrate_lto_expiry(self, establishment):
        return establishment.ltos.latest().expiry

    class Meta:
        model=Establishment
        fields = ('name', 'lto', 'lto_expiry', 'primary_activity__name', 'plant_address__address',
        'plant_address__province__name', 'plant_address__municipality_or_city__name', 'specific_activities', )

        # def dehydrate_specific_activity(self, establishment):
        #     return '%s by %s' % (establishment.)
