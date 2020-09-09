from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User, UserDesignation

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 'email', 'get_full_name', 'designations', 'active', 'staff', 'admin',)
    list_filter = ('admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'middle_initial', 'last_name')}),
        ('Permissions', {'fields': ('admin', 'staff', 'active',)}),
        ('Designation', {'fields': ('designation',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
        ('Personal info', {'fields': ('first_name', 'middle_initial', 'last_name')}),
        ('Permissions', {'fields': ('admin', 'staff', 'active',)}),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

    def designations(self, obj):
        return ",\n".join(s.name for s in obj.designation.all())

    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Full Name'


admin.site.register(User, UserAdmin)
admin.site.register(UserDesignation)
