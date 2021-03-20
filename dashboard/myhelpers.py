from masterlist.models import Establishment, ProductType
from pms.models import Product
from pli.models import Pli
from appsreceived.models import Application
# from django.db.models import Q

class MasterlistSummaryHelper:
    model = ''
    center = ''
    product_type = ''
    province_or_city = ''
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
            'product_type': self.product_type,
            'status':       'Active',
        }

        if 'province_or_city' in kwargs:
            self.province_or_city = kwargs['province_or_city']
            if kwargs['province_or_city'] == 'Baguio City':
                self.filters['plant_address__municipality_or_city__name'] = kwargs['province_or_city']
            else:
                self.filters['plant_address__province__name'] = kwargs['province_or_city']
        return self.filters

    def get_total(self):
        count = 0
        count_bag = Establishment.objects.filter(
            status='Active',
            product_type=self.product_type,
            plant_address__municipality_or_city__name='Baguio City'
        ).count()

        if self.province_or_city == '':
            count = Establishment.objects.filter(
                status='Active',
                product_type=self.product_type,
            ).count()
        elif self.province_or_city == 'Baguio City':
            count = count_bag
        elif self.province_or_city == 'Benguet':
            count_ben = Establishment.objects.filter(
                status='Active',
                product_type=self.product_type,
                plant_address__province__name=self.province_or_city,
            ).count()

            count = count_ben - count_bag
        else:
            count = Establishment.objects.filter(
                status='Active',
                product_type=self.product_type,
                plant_address__province__name=self.province_or_city,
            ).count()

        return abs(count)

    def get_total_mfg(self):
        count = self.get_prim_total('Manufacturer')
        return count

    def get_total_packer(self):
        count = self.get_prim_total('Packer')
        return count

    def get_total_repacker(self):
        count = self.get_prim_total('Repacker')
        return count

    def get_total_trader(self):
        count = self.get_prim_total('Trader')
        return count

    def get_total_m_p_r_t(self):
        count = self.get_total_mfg() + self.get_total_packer() + self.get_total_repacker() + self.get_total_trader()
        return count

    def get_total_wholesaler(self):
        return self.get_spec_total(spec_activ='Wholesaler', exclude1='Importer', exclude2='Exporter')

    def get_total_importer(self):
        return self.get_spec_total(spec_activ='Importer', exclude1='Wholesaler', exclude2='Exporter')

    def get_total_exporter(self):
        return self.get_spec_total(spec_activ='Exporter', exclude1='Wholesaler', exclude2='Importer')

    def get_total_wi(self):
        count = 0
        count_bag = Establishment.objects.filter(
                        product_type=self.product_type,
                        status='Active',
                        specific_activity__name='Wholesaler',
                        plant_address__municipality_or_city__name='Baguio City',
                    ).filter(specific_activity__name='Importer').exclude(specific_activity__name='Exporter').count()

        if self.province_or_city == 'Baguio City':
            count = count_bag
        elif self.province_or_city == 'Benguet':
            count_ben = Establishment.objects.filter(
                        product_type=self.product_type,
                        status='Active',
                        specific_activity__name='Wholesaler',
                        plant_address__province__name='Benguet',
                    ).filter(specific_activity__name='Importer').exclude(specific_activity__name='Exporter').count()

            count = count_ben - count_bag
        elif self.province_or_city == '':
            count = Establishment.objects.filter(
                    product_type=self.product_type,
                    status='Active',
                    specific_activity__name='Wholesaler',
            ).filter(specific_activity__name='Importer').exclude(specific_activity__name='Exporter').count()
        else:
            count = Establishment.objects.filter(
                    product_type=self.product_type,
                    status='Active',
                    specific_activity__name='Wholesaler',
                    plant_address__province__name=self.province_or_city,
            ).filter(specific_activity__name='Importer').exclude(specific_activity__name='Exporter').count()

        return abs(count)

    def get_total_we(self):
        count = 0
        count_bag = Establishment.objects.filter(
                        product_type=self.product_type,
                        status='Active',
                        specific_activity__name='Wholesaler',
                        plant_address__municipality_or_city__name='Baguio City',
                    ).filter(specific_activity__name='Exporter').exclude(specific_activity__name='Importer').count()

        if self.province_or_city == 'Baguio City':
            count = count_bag
        elif self.province_or_city == 'Benguet':
            count_ben = Establishment.objects.filter(
                    product_type=self.product_type,
                    status='Active',
                    specific_activity__name='Wholesaler',
                    plant_address__province__name='Benguet',
            ).filter(specific_activity__name='Exporter').exclude(specific_activity__name='Importer').count()

            count = count_ben - count_bag
        elif self.province_or_city == '':
            count = Establishment.objects.filter(
                    product_type=self.product_type,
                    status='Active',
                    specific_activity__name='Wholesaler',
            ).filter(specific_activity__name='Exporter').exclude(specific_activity__name='Importer').count()
        else:
            count = Establishment.objects.filter(
                    product_type=self.product_type,
                    status='Active',
                    specific_activity__name='Wholesaler',
                    plant_address__province__name=self.province_or_city,
            ).filter(specific_activity__name='Exporter').exclude(specific_activity__name='Importer').count()

        return abs(count)

    def get_total_ie(self):
        count = 0
        count_bag = Establishment.objects.filter(
                        product_type=self.product_type,
                        status='Active',
                        specific_activity__name='Importer',
                        plant_address__municipality_or_city__name='Baguio City',
                    ).filter(specific_activity__name='Exporter').exclude(specific_activity__name='Wholesaler').count()

        if self.province_or_city == 'Baguio City':
            count = count_bag
        elif self.province_or_city == 'Benguet':
            count_ben = Establishment.objects.filter(
                    product_type=self.product_type,
                    status='Active',
                    specific_activity__name='Importer',
                    plant_address__province__name='Benguet',
            ).filter(specific_activity__name='Exporter').exclude(specific_activity__name='Wholesaler').count()

            count = count_ben - count_bag
        elif self.province_or_city == '':
            count = Establishment.objects.filter(
                    product_type=self.product_type,
                    status='Active',
                    specific_activity__name='Importer',
            ).filter(specific_activity__name='Exporter').exclude(specific_activity__name='Wholesaler').count()
        else:
            count = Establishment.objects.filter(
                    product_type=self.product_type,
                    status='Active',
                    specific_activity__name='Importer',
                    plant_address__province__name=self.province_or_city,
            ).filter(specific_activity__name='Exporter').exclude(specific_activity__name='Wholesaler').count()

        return abs(count)

    def get_total_wei(self):
        count = 0
        count_bag = Establishment.objects.filter(
                        product_type=self.product_type,
                        status='Active',
                        specific_activity__name='Wholesaler',
                        plant_address__municipality_or_city__name='Baguio City',
                    ).filter(specific_activity__name='Importer').filter(specific_activity__name='Exporter').count()

        if self.province_or_city == 'Baguio City':
            count = count_bag
        elif self.province_or_city == 'Benguet':
            count_ben = Establishment.objects.filter(
                    product_type=self.product_type,
                    status='Active',
                    specific_activity__name='Wholesaler',
                    plant_address__province__name='Benguet',
            ).filter(specific_activity__name='Importer').filter(specific_activity__name='Exporter').count()

            count = count_ben - count_bag
        elif self.province_or_city == '':
            count = Establishment.objects.filter(
                    product_type=self.product_type,
                    status='Active',
                    specific_activity__name='Wholesaler',
            ).filter(specific_activity__name='Importer').filter(specific_activity__name='Exporter').count()
        else:
            count = Establishment.objects.filter(
                    product_type=self.product_type,
                    status='Active',
                    specific_activity__name='Wholesaler',
                    plant_address__province__name=self.province_or_city,
            ).filter(specific_activity__name='Importer').filter(specific_activity__name='Exporter').count()

        return abs(count)

    def get_total_dist(self):
        count = 0
        count = self.get_total_wholesaler() + self.get_total_importer() + self.get_total_exporter() + self.get_total_we() + self.get_total_wi() + self.get_total_ie() + self.get_total_wei()
        return count

    def get_filtered(self):
        return Establishment.objects.filter(**self.filters)

    def get_filtered_total(self):
        return self.get_filtered().count()

    def get_prim_total(self, prim_activ):
        count = 0
        count_bag = Establishment.objects.filter(
            product_type=self.product_type,
            status='Active',
            primary_activity__name=prim_activ,
            plant_address__municipality_or_city__name='Baguio City',
        ).count()

        if self.province_or_city == '':
            count = Establishment.objects.filter(
                status='Active',
                product_type=self.product_type,
                primary_activity__name=prim_activ
            ).count()
        elif self.province_or_city == 'Baguio City':
            count = count_bag
        elif self.province_or_city == 'Benguet':
            count_ben = Establishment.objects.filter(
                product_type=self.product_type,
                status='Active',
                primary_activity__name=prim_activ,
                plant_address__province__name='Benguet',
            ).count()

            count = count_ben - count_bag
        else:
            count = Establishment.objects.filter(
                product_type=self.product_type,
                status='Active',
                primary_activity__name=prim_activ,
                plant_address__province__name=self.province_or_city,
            ).count()

        return abs(count)

    def get_spec_total(self, spec_activ, exclude1, exclude2):
        count = 0
        count_bag = Establishment.objects.filter(
            product_type=self.product_type,
            status='Active',
            specific_activity__name=spec_activ,
            plant_address__municipality_or_city__name='Baguio City',
        ).exclude(specific_activity__name=exclude1).exclude(specific_activity__name=exclude2).count()

        if self.province_or_city == '':
            count = Establishment.objects.filter(
                product_type=self.product_type,
                status='Active',
                specific_activity__name=spec_activ,
            ).exclude(specific_activity__name=exclude1).exclude(specific_activity__name=exclude2).count()
        elif self.province_or_city == 'Baguio City':
            count = count_bag
        elif self.province_or_city == 'Benguet':
            count_ben = Establishment.objects.filter(
                product_type=self.product_type,
                status='Active',
                specific_activity__name=spec_activ,
                plant_address__province__name='Benguet',
            ).exclude(specific_activity__name=exclude1).exclude(specific_activity__name=exclude2).count()

            count = count_ben - count_bag
        else:
            count = Establishment.objects.filter(
                product_type=self.product_type,
                status='Active',
                specific_activity__name=spec_activ,
                plant_address__province__name=self.province_or_city,
            ).exclude(specific_activity__name=exclude1).exclude(specific_activity__name=exclude2).count()

        return abs(count)

    def get_spec_total_single(self, spec_activ):
        count = 0
        count_bag = Establishment.objects.filter(
            product_type=self.product_type,
            status='Active',
            specific_activity__name=spec_activ,
            plant_address__municipality_or_city__name='Baguio City',
        ).count()

        if self.province_or_city == '':
            count = Establishment.objects.filter(
                product_type=self.product_type,
                status='Active',
                specific_activity__name=spec_activ
            ).count()
        elif self.province_or_city == 'Baguio City':
            count = count_bag
        elif self.province_or_city == 'Benguet':
            count_ben = Establishment.objects.filter(
                product_type=self.product_type,
                status='Active',
                specific_activity__name=spec_activ,
                plant_address__province__name='Benguet',
            ).count()

            count = count_ben - count_bag
        else:
            count = Establishment.objects.filter(
                product_type=self.product_type,
                status='Active',
                specific_activity__name=spec_activ,
                plant_address__province__name=self.province_or_city,
            ).count()

        return abs(count)

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
            return super().get_spec_total_single('Hospital Pharmacy')

        def get_total_ds(self):
            return super().get_spec_total_single('Drugstore')

        def get_total_ronpd(self):
            return super().get_spec_total_single('Retail Outlet for Non-Prescription Drugs')

        def get_total_ds_ronpd(self):
            return self.get_total_ds() + self.get_total_ronpd()

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
            med_xray = super().get_spec_total_single('Medical X-Ray')
            vet_xray = super().get_spec_total_single('Veterinary X-Ray')
            den_xray = super().get_spec_total_single('Dental X-Ray')
            mri_xray = super().get_spec_total_single('MRI')
            edu_xray = super().get_spec_total_single('Educational X-Ray')
            ctscan_xray = super().get_spec_total_single('CTScan')
            mobile_xray = super().get_spec_total_single('Mobile X-Ray')
            non_medical_xray = super().get_spec_total_single('Non-Medical X-Ray')
            return med_xray + vet_xray + den_xray + mri_xray + edu_xray + ctscan_xray + mobile_xray + non_medical_xray

class Province:

    province_or_city = ''

    def __init__(self, province_or_city):
        self.province_or_city = province_or_city

    def get_total(self):
        if self.province_or_city=='Baguio City':
            return Establishment.objects.filter(plant_address__municipality_or_city__name=self.province_or_city, status='Active').count()
        elif self.province_or_city=='Benguet':
            return Establishment.objects.filter(plant_address__province__name=self.province_or_city, status='Active').exclude(plant_address__municipality_or_city__name='Baguio City').count()

        return Establishment.objects.filter(plant_address__province__name=self.province_or_city, status='Active').count()

    def cfrr(self):
        return Center.Cfrr(center='CFRR', province_or_city=self.province_or_city)

    def cdrr(self):
        return Center.Cdrr(center='CDRR', province_or_city=self.province_or_city)

    def ccrr(self):
        return Center.Ccrr(center='CCRR', province_or_city=self.province_or_city)

    def cdrrhr(self):
        return Center.Cdrrhr(center='CDRRHR', province_or_city=self.province_or_city)

class Pendings:

    def get_total_expired(self):
        except_activities = ['Hospital Pharmacy', 'Medical X-Ray', 'Veterinary X-Ray', 'Dental X-Ray', 'Educational X-Ray', 'MRI', 'CTScan', 'Mobile X-Ray']
        total = Establishment.expiredlist.get_list().exclude(specific_activity__name__in=except_activities).order_by('name').count()
        return total

    def get_total_awaiting_result(self):
        total = Product.objects.filter(status='Awaiting Result').count()
        return total

    def get_total_awaiting_closure(self):
        total = Pli.objects.filter(status__status = 'Awaiting Letter of Closure').count()
        return total

    def get_total_awaiting_capa(self):
        total_apps = Application.objects.filter(status='Returned to Client').count()
        total_pli = Pli.objects.filter(status__status='Awaiting CAPA').count()
        total = total_apps + total_pli
        return total
