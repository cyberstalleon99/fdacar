from import_export import resources
from import_export.fields import Field
from .models import Establishment, Lto
from checklist.models import Job
from dateutil.relativedelta import relativedelta

class EstablishmentResource(resources.ModelResource):
    name = Field(attribute="name", column_name="Establishment Name")
    product_type = Field(attribute="product_type__name", column_name="Product Type")
    primary_activity = Field(attribute="primary_activity__name", column_name="Primary Activity")
    specific_activity = Field(column_name="Specific Activity/s")
    product_line = Field(column_name="Product Line")
    remarks = Field(column_name="Products")
    lto = Field(column_name="LTO Number")
    lto_expiry = Field(column_name="Expiry")
    plant_address = Field(attribute="plant_address__address", column_name="Address")
    province = Field(attribute="plant_address__province__name", column_name="Province")
    municipality_or_city = Field(attribute="plant_address__municipality_or_city__name", column_name="City or Municipality")
    owner = Field(column_name="Owner")
    qualified_person = Field(column_name="Qualified Person/s")
    contact_number = Field(attribute="authorized_officer__mobile", column_name="Contact Number")
    email = Field(attribute="authorized_officer__email", column_name="Email Address")
    last_inspection = Field(column_name="Last Inspection")
    frequency_of_inspection = Field(column_name="Frequency of Inspection")
    next_inspection = Field(column_name="Next Inspection")
    type_of_inspection = Field(column_name="Type of Inspection")
    inspected_by = Field(column_name="Inspector")
    status = Field(attribute="status", column_name="Status")
    folder_id = Field(column_name="Folder Number")

    def dehydrate_specific_activity(self, establishment):
        return ",\n".join(activity.name  for activity in establishment.specific_activity.all())

    def dehydrate_lto(self, establishment):
        try:
            establishment.ltos.latest()
        except:
            return None
        else:
            return establishment.ltos.latest()

    def dehydrate_lto_expiry(self, establishment):
        try:
            establishment.ltos.latest().expiry
        except:
            return None
        else:
            return establishment.ltos.latest().expiry

    def dehydrate_product_line(self, establishment):
        # product_lines = ''
        # for prod_line in establishment.product_lines.all():
        #     product_lines += prod_line.product_line.name + ", "
        # return product_lines
        return ",\n".join(product_line.product_line.name  for product_line in establishment.product_lines.all())

    def dehydrate_qualified_person(self, establishment):
        return ",\n".join(person.full_name()  for person in establishment.qualifiedperson_set.all())

    def dehydrate_owner(self, establishment):
        return establishment.authorized_officer.full_name()

    def dehydrate_remarks(self, establishment):
        product_remarks = ''
        for prod_line in establishment.product_lines.all():
            if prod_line.remarks:
                product_remarks += prod_line.remarks + ", "
        return product_remarks
        # return ",\n".join(product_line.remarks  for product_line in establishment.product_lines.all())

    def dehydrate_last_inspection(self, establishment):
        try:
            establishment.record.inspections.latest().date_inspected
        except:
            return 'For inspection'
        else:
            return establishment.record.inspections.latest().date_inspected

    def dehydrate_frequency_of_inspection(self, establishment):
        try:
            establishment.record.inspections.latest().date_inspected
        except:
            return 'For inspection'
        else:
            frequency_of_inspection = establishment.record.inspections.latest().frequency_of_inspection
            if frequency_of_inspection:
                return establishment.record.inspections.latest().frequency_of_inspection
            else:
                return 'No Risk Assessment'

    def dehydrate_type_of_inspection(self, establishment):

        try:
            establishment.record.inspections.latest().date_inspected
        except:
            return 'For inspection'
        else:
            return establishment.record.inspections.latest().inspection_type

    def dehydrate_next_inspection(self, establishment):
        next_date_inspection = ''

        try:
            establishment.record.inspections.latest()
        except:
            return 'No inspections yet'
        else:
            frequency_of_inspection = establishment.record.inspections.latest().frequency_of_inspection
            if frequency_of_inspection:
                next_date_inspection = establishment.record.inspections.latest().date_inspected + relativedelta(years=int(frequency_of_inspection))
            else:
                return 'No Risk Assessment'
        return next_date_inspection

    def dehydrate_inspected_by(self, establishment):
        try:
            establishment.record.inspections.latest().date_inspected
        except:
            return 'For inspection'
        else:
            return ",\n".join(inspector.inspector.get_short_name()  for inspector in establishment.record.inspections.latest().est_inspectors.all())

    def dehydrate_folder_id(self, establishment):

        try:
            establishment.record
        except:
            return 'No file'
        else:
            return establishment.record.folder_id

    class Meta:
        model=Establishment
        exclude = ('id', 'date_modified', 'application', 'center', 'additional_activity', 'office_address', 'authorized_officer', 'modified_by')

class JobResource(resources.ModelResource):
    name = Field(attribute="establishment__name", column_name="Establishment Name")
    product_type = Field(attribute="establishment__product_type__name", column_name="Product Type")
    primary_activity = Field(attribute="establishment__primary_activity__name", column_name="Primary Activity")
    specific_activity = Field(column_name="Specific Activity/s")
    product_line = Field(column_name="Product Line")
    remarks = Field(attribute="establishment__remarks", column_name="Product Remarks")
    lto = Field(column_name="LTO Number")
    lto_expiry = Field(column_name="Expiry")
    plant_address = Field(attribute="establishment__plant_address__address", column_name="Address")
    province = Field(attribute="establishment__plant_address__province__name", column_name="Province")
    municipality_or_city = Field(attribute="establishment__plant_address__municipality_or_city__name", column_name="City or Municipality")
    contact_number = Field(attribute="establishment__authorized_officer__mobile", column_name="Contact Number")
    email = Field(attribute="establishment__authorized_officer__email", column_name="Email Address")
    status = Field(attribute="establishment__status", column_name="Status")
    # folder_id = Field(column_name="Folder Number")

    def dehydrate_specific_activity(self, job):
        specific_activities = ''
        for spec_act in job.establishment.specific_activity.all():
            specific_activities += spec_act.name + ", "
        return specific_activities

    def dehydrate_lto(self, job):
        try:
            job.establishment.ltos.latest()
        except:
            return "N/A"
        else:
            return job.establishment.ltos.latest()

    def dehydrate_lto_expiry(self, job):
        try:
            job.establishment.ltos.latest().expiry
        except:
            return "N/A"
        else:
            return job.establishment.ltos.latest().expiry

    def dehydrate_product_line(self, job):
        product_lines = ''
        for prod_line in job.establishment.product_lines.all():
            product_lines += prod_line.product_line.name + ", "
        return product_lines

    def dehydrate_remarks(self, job):
        product_remarks = ''
        for prod_line in job.establishment.product_lines.all():
            if prod_line.remarks:
                product_remarks += prod_line.remarks + ", "
        return product_remarks

    # def dehydrate_folder_id(self, job):
    #     try:
    #         job.establishment.record
    #     except:
    #         return 'No file'
    #     else:
    #         return job.establishment.record.folder_id

    class Meta:
        model=Job
        exclude = ('id', 'date_modified', 'application', 'center', 'additional_activity', 'office_address', 'authorized_officer',)

class LtoResource(resources.ModelResource):
    # ('lto_number', 'type_of_application', 'issuance', 'expiry',
    # 'name', 'address', 'city_or_municipality', 'inspections')
    lto_number = Field(column_name="LTO #")
    type_of_application = Field(attribute="type_of_application", column_name="Application Type")
    issuance = Field(attribute="issuance", column_name="Issuance")
    expiry = Field(column_name="Expiry")
    name = Field(column_name="Establishment")
    address = Field(column_name="Address")
    city_or_municipality = Field(column_name="City or Municipality")
    province = Field(column_name="Province")
    primary_activity = Field(column_name="Primary Activity")
    specific_activity = Field(column_name="Specific Activity")
    inspections = Field(column_name="PLI Inspections (2018-Present)")
    status = Field(column_name="Status")
    folder_number = Field(column_name="Folder #")

    def dehydrate_lto_number(self, lto):
        return lto.establishment.ltos.latest()

    def dehydrate_expiry(self, lto):
        return lto.establishment.ltos.latest().expiry

    def dehydrate_name(self, lto):
        return lto.establishment.name

    def dehydrate_address(self, lto):
        return lto.establishment.plant_address.address

    def dehydrate_city_or_municipality(self, lto):
        return lto.establishment.plant_address.municipality_or_city

    def dehydrate_province(self, lto):
        return lto.establishment.plant_address.province.name

    def dehydrate_primary_activity(self, lto):
        return lto.establishment.primary_activity.name

    def dehydrate_specific_activity(self, lto):
         return lto.establishment.specific_activities()

    def dehydrate_inspections(self, lto):
        try:
            lto.establishment.record.inspections.all()
        except:
            return 'No inspections'
        else:
            inspections = lto.establishment.record.inspections.filter(inspection_type__name='Post Licensing Inspection', date_inspected__gte='2018-01-01')
            return ", \n".join(s.date_inspected.strftime('%d %b %Y') + ' - ' + s.inspection_type.name for s in inspections)

    def dehydrate_status(self, lto):
        return lto.establishment.status

    def dehydrate_folder_number(self, lto):
        try:
            lto.establishment.record.inspections.all()
        except:
            return 'No Folder'
        else:
            return lto.establishment.record.folder_id

    class Meta:
        model = Lto
        exclude = ('id', 'establishment',)