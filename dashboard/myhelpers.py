from masterlist.models import Establishment, ProductType

class MasterlistSummaryHelper:
    model = ''
    center = ''
    product_type = ''
    filters = {}

    def __init__(self, center, **kwargs):
        self.center = center
        if self.center == 'CFRR':
            self.product_type = ProductType.objects.get(name='Food')
        elif self.center == 'CDRR':
            self.product_type = ProductType.objects.get(name='Drug')
        elif self.center == 'CCRR':
            self.product_type = ProductType.objects.get(name='Cosmetic')
        elif self.center == 'CDRRHR':
            self.product_type = ProductType.objects.get(name='Medical Device')

        self.init_filters(**kwargs)


    def init_filters(self, **kwargs):
        # Default filters
        self.filters = {
            'product_type':self.product_type,
            'status': 'Active',
        }

        if 'province_or_city' in kwargs:
            if kwargs['province_or_city'] == 'Baguio City':
                self.filters['plant_address__municipality_or_city__name'] = kwargs['province_or_city']
            else:
                self.filters['plant_address__province__name'] = kwargs['province_or_city']

    def get_total(self):
        print(self.filters)
        return self.get_filtered_total()

    def get_total_mfg(self):
        self.filters['primary_activity__name'] = 'Manufacturer'
        print(self.filters)
        return self.get_filtered_total()

    def get_total_trader(self):
        self.filters['primary_activity__name'] = 'Trader'
        print(self.filters)
        return self.get_filtered_total()

    def get_total_wholesaler(self):
        self.filters.pop('primary_activity__name', 'Nothing found') # remove primary_activity__name from default filter so it won't conflict with specific_activity__name
        self.filters['specific_activity__name'] = "Wholesaler"
        print(self.filters)
        return self.get_filtered_total()

    def get_total_importer(self):
        self.filters['specific_activity__name'] = 'Importer'
        print(self.filters)
        return self.get_filtered_total()

    def get_total_exporter(self):
        self.filters['specific_activity__name'] = 'Exporter'
        print(self.filters)
        return self.get_filtered_total()


    def get_filtered(self):
        return Establishment.objects.filter(**self.filters)

    def get_filtered_total(self):
        return self.get_filtered().count()

class Center:

    class Cfrr(MasterlistSummaryHelper):

        def __init__(self, **kwargs):
            if 'province_or_city' in kwargs:
                super().__init__(center='CFRR', province_or_city=kwargs['province_or_city'])
            else:
                super().__init__(center='CFRR')


    class Cdrr(MasterlistSummaryHelper):

        def __init__(self, **kwargs):
            if 'province_or_city' in kwargs:
                super().__init__(center='CDRR', province_or_city=kwargs['province_or_city'])
            else:
                super().__init__(center='CDRR')

        def get_total_hp(self):
            return Establishment.objects.filter(product_type=self.product_type, specific_activity__name='Hospital Pharmacy', status='Active').count()

        def get_total_ds(self):
            ds = Establishment.objects.filter(product_type=self.product_type, specific_activity__name='Drugstore', status='Active').count()
            ronpd = Establishment.objects.filter(product_type=self.product_type, specific_activity__name='Retail Outlet for Non-Prescription Drugs', status='Active').count()
            return ds + ronpd

    class Ccrr(MasterlistSummaryHelper):

        def __init__(self, **kwargs):
            if 'province_or_city' in kwargs:
                super().__init__(center='CCRR', province_or_city=kwargs['province_or_city'])
            else:
                super().__init__(center='CCRR')

    class Cdrrhr(MasterlistSummaryHelper):

        def __init__(self, **kwargs):
            if 'province_or_city' in kwargs:
                super().__init__(center='CDRRHR', province_or_city=kwargs['province_or_city'])
            else:
                super().__init__(center='CDRRHR')

        def get_total_xray(self):
            med_xray = Establishment.objects.filter(product_type=self.product_type, specific_activity__name='Medical X-Ray', status='Active').count()
            vet_xray = Establishment.objects.filter(product_type=self.product_type, specific_activity__name='Veterinary X-Ray', status='Active').count()
            den_xray = Establishment.objects.filter(product_type=self.product_type, specific_activity__name='Dental X-Ray', status='Active').count()
            mri_xray = Establishment.objects.filter(product_type=self.product_type, specific_activity__name='MRI', status='Active').count()
            edu_xray = Establishment.objects.filter(product_type=self.product_type, specific_activity__name='Educational X-Ray', status='Active').count()
            ctscan_xray = Establishment.objects.filter(product_type=self.product_type, specific_activity__name='CTScan', status='Active').count()
            return med_xray + vet_xray + den_xray + mri_xray + edu_xray + ctscan_xray

class Province:

    province_or_city = ''

    def __init__(self, province_or_city):
        self.province_or_city = province_or_city

    def get_total(self):
        return Establishment.objects.filter(plant_address__province__name=self.province_or_city, status='Active').count()

    def cfrr(self):
        return Center.Cfrr(center='CFRR', province_or_city=self.province_or_city)

    def cdrr(self):
        return Center.Cdrr(center='CDRR', province_or_city=self.province_or_city)

    def ccrr(self):
        return Center.Ccrr(center='CCRR', province_or_city=self.province_or_city)

    def cdrrhr(self):
        return Center.Cdrrhr(center='CDRRHR', province_or_city=self.province_or_city)
