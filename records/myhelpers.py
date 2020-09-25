from records.models import Record
import re

class Folder:

    new_folder = ''

    product_type = ''
    prim_activity = ''
    spec_activities = ''
    province = ''
    city_or_municip = ''

    last_number = ''
    new_number = ''

    first_param = ''
    second_param = ''
    third_param = ''

    spec_activities_list = ''

    def __init__(self, establishment):
        self.product_type =      establishment.product_type.name
        self.prim_activity =     establishment.primary_activity.name
        self.spec_activities =   establishment.specific_activity.all()
        self.province =          establishment.plant_address.province
        self.city_or_municip =   establishment.plant_address.municipality_or_city.name
        self.spec_activities_list = list(establishment.specific_activity.all())

    def get_next_number(self):
        filters = {}
        records = ''
        filters = {
            'establishment__product_type__name': self.product_type,
            'establishment__primary_activity__name': self.prim_activity,
            'establishment__plant_address__province': self.province,
            'establishment__plant_address__municipality_or_city__name': self.city_or_municip,
            'establishment__specific_activity': self.spec_activities_list[0]
        }
        records = Record.objects.filter(**filters).order_by('folder_id')

        if len(self.spec_activities_list) == 2:
            filter1 = {'establishment__specific_activity': self.spec_activities_list[1]}
            records = Record.objects.filter(**filters).filter(**filter1).order_by('folder_id')

        elif len(self.spec_activities_list) == 3:
            filter2 = {'establishment__specific_activity': self.spec_activities_list[1]}
            filter3 = {'establishment__specific_activity': self.spec_activities_list[2]}
            records = Record.objects.filter(**filters).filter(**filter2).filter(**filter3).order_by('folder_id')

        try:
            records.last().folder_id
        except:
            last_folder = '0'
        else:
            last_folder = records.last().folder_id
        temp = re.findall(r'\d+', last_folder)
        last_number_list = list(map(int, temp))
        self.last_number = int("".join(map(str, last_number_list))) + 1

        if self.last_number < 10:
            self.last_number = '0' + str(self.last_number)

        return self.last_number

    def get_first_param(self):
        self.first_param = self.product_type[0]
        return self.first_param

    def get_second_param(self):
        if self.prim_activity == 'Retailer':
            if self.spec_activities_list[0] == 'Drugstore':
                self.second_param = 'S'
            else:
                self.second_param = 'X'
        elif self.prim_activity == 'Distributor':
            self.second_param = "/".join(specific_activity.name[0] for specific_activity in list(self.spec_activities))
        else:
            self.second_param = self.prim_activity[0]

        return self.second_param

    def get_thrid_param(self):
        if self.city_or_municip == 'Baguio City':
            self.third_param = 'BAG'
        else:
            self.third_param = self.province.short_name
        return self.third_param

    def create_folder(self):
        self.new_folder = self.get_first_param() + self.get_second_param() + self.get_thrid_param() + '-' + self.get_next_number()
        return self.new_folder

