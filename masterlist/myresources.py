from import_export import resources, fields
from .models import Establishment, SpecificActivity, Lto
from import_export.widgets import ManyToManyWidget, ForeignKeyWidget

class EstablishmentResource(resources.ModelResource):
    specific_activity = fields.Field(widget=ManyToManyWidget(SpecificActivity, field='name'))
    lto = fields.Field(column_name="LTO", widget=ForeignKeyWidget(Lto))

    class Meta:
        model=Establishment
        fields = ('name', 'lto', 'primary_activity__name', 'plant_address__address',
        'plant_address__province__name', 'plant_address__municipality_or_city__name', 'specific_activity', )

        # def dehydrate_specific_activity(self, establishment):
        #     return '%s by %s' % (establishment.)
