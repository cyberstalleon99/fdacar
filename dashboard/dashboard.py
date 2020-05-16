from masterlist.models import Establishment, PrimaryActivity, ProductType, SpecificActivity

def get_primary_acitivity_obj(primary_activity_name):
    return PrimaryActivity.objects.get(name=primary_activity_name)

def get_specific_acitivity_obj(specific_activity_name):
    return SpecificActivity.objects.get(name=specific_activity_name)

class MasterlistSummaryHelper:
    model = ''
    center = ''
    product_type = ''

    def __init__(self, center):
        self.center = center
        if self.center == 'CFRR':
            self.product_type = ProductType.objects.get(name='Food')
        elif self.center == 'CDRR':
            self.product_type = ProductType.objects.get(name='Drug')
        elif self.center == 'CCRR':
            self.product_type = ProductType.objects.get(name='Cosmetic')
        elif self.center == 'CDRRHR':
            self.product_type = ProductType.objects.get(name='Medical Device')

    def get_total(self):
        return Establishment.objects.filter(center=self.center, status='Active').count()

    def get_total_mfg(self):
        return Establishment.objects.filter(product_type=self.product_type, primary_activity=get_primary_acitivity_obj('Manufacturer'), status='Active').count()

    def get_total_trader(self):
        return Establishment.objects.filter(product_type=self.product_type, primary_activity=get_primary_acitivity_obj('Trader'), status='Active').count()

    def get_total_wholesaler(self):
        return Establishment.objects.filter(product_type=self.product_type, specific_activity=get_specific_acitivity_obj('Wholesaler'), status='Active').count()

    def get_total_importer(self):
            return Establishment.objects.filter(product_type=self.product_type, specific_activity=get_specific_acitivity_obj('Importer'), status='Active').count()

    def get_total_exporter(self):
            return Establishment.objects.filter(product_type=self.product_type, specific_activity=get_specific_acitivity_obj('Exporter'), status='Active').count()

class MasterlistSummary:

    class CFRR(MasterlistSummaryHelper):
        pass

    class CDRR(MasterlistSummaryHelper):

        def get_total_hp(self):
            return Establishment.objects.filter(product_type=self.product_type, specific_activity=get_specific_acitivity_obj('Hospital Pharmacy'), status='Active').count()

        def get_total_ds(self):
            ds = Establishment.objects.filter(product_type=self.product_type, specific_activity=get_specific_acitivity_obj('Drugstore'), status='Active').count()
            ronpd = Establishment.objects.filter(product_type=self.product_type, specific_activity=get_specific_acitivity_obj('Retail Outlet for Non-Prescription Drugs'), status='Active').count()
            return ds + ronpd

    class CCRR(MasterlistSummaryHelper):
        pass

    class CDRRHR(MasterlistSummaryHelper):

        def get_total_xray(self):
            med_xray = Establishment.objects.filter(product_type=self.product_type, specific_activity=get_specific_acitivity_obj('Medical X-Ray'), status='Active').count()
            vet_xray = Establishment.objects.filter(product_type=self.product_type, specific_activity=get_specific_acitivity_obj('Veterinary X-Ray'), status='Active').count()
            den_xray = Establishment.objects.filter(product_type=self.product_type, specific_activity=get_specific_acitivity_obj('Dental X-Ray'), status='Active').count()
            mri_xray = Establishment.objects.filter(product_type=self.product_type, specific_activity=get_specific_acitivity_obj('MRI'), status='Active').count()
            edu_xray = Establishment.objects.filter(product_type=self.product_type, specific_activity=get_specific_acitivity_obj('Educational X-Ray'), status='Active').count()
            ctscan_xray = Establishment.objects.filter(product_type=self.product_type, specific_activity=get_specific_acitivity_obj('CTScan'), status='Active').count()
            return med_xray + vet_xray + den_xray + mri_xray + edu_xray + ctscan_xray
