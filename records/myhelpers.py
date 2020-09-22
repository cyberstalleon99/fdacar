from masterlist.models import PrimaryActivity, SpecificActivity


def create_folder(establishment):
    new_folder = ''

    product_type =      establishment.product_type.name
    prim_activity =     establishment.primary_activity.name
    spec_activities =   list(establishment.specific_activities())
    short_prov =        establishment.plant_address.province.short_name
    city_or_municip =   establishment.plant_address.municipality_or_city.name

    prims = list(PrimaryActivity.objects.all())
    specs = list(SpecificActivity.objects.all())

