from django.contrib import admin
from accounts.models import User
from .models import (Product, Classification, ReferralType, ProductCategory, DosageForm, CollectionMode,
AnalysisRequest, Unit, ProductEstablishment, ProductAddress, ProductSpecificActivity, ProductInspector)
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter
from import_export.admin import ExportActionModelAdmin
from .myresources import ProductResource


admin.site.register(Classification)
admin.site.register(ReferralType)
admin.site.register(ProductCategory)
admin.site.register(DosageForm)
admin.site.register(CollectionMode)
admin.site.register(AnalysisRequest)
admin.site.register(Unit)
admin.site.register(ProductEstablishment)
admin.site.register(ProductAddress)
admin.site.register(ProductSpecificActivity)

# Custom Filter
class InspectorFilter(admin.SimpleListFilter):
    template = 'django_admin_listfilter_dropdown/dropdown_filter.html'
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Inspector'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'inspector'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        filts = []
        users = User.objects.all()
        for inspector in users:
            filts.append([inspector.id, inspector.get_short_name()])

        return filts

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.

        if self.value():
            return queryset.filter(product_inspectors__product_inspector__id=self.value())
        else:
            return queryset


class InspectorInline(admin.TabularInline):
    model = ProductInspector
    extra = 1

@admin.register(Product)
class ProductAdmin(ExportActionModelAdmin, admin.ModelAdmin):

    inlines = (InspectorInline,)
    list_per_page = 20
    ordering = ('-group',)
    resource_class = ProductResource

    list_display = ('status', 'generic_name', 'brand_name', 'month', 'date_collected', 'tracking_number',
                    'classification', 'type_of_referral', 'analysis_request', 'establishment', 'address',
                    'product_category', 'collection_mode', 'inspector', 'date_forwarded', 'date_result_received', 'result',
                    'center_remarks',
    )

    list_filter = (
        ('status', DropdownFilter),
        (InspectorFilter),
        ('group', DropdownFilter),
        ('type_of_referral', RelatedDropdownFilter),
        ('result', DropdownFilter),
    )

    def __str__(self, product):
        return product.generic_name + " - " + product.tracking_number


    def month(self, product):
        return product.group.strftime('%B')

    def establishment(self, product):
        return product.establishment.name

    def address(self, product):
        return product.establishment.address.full_address()

    def inspector(self, product):
        return ",\n".join(s.product_inspector.get_short_name()  for s in product.product_inspectors.all())


