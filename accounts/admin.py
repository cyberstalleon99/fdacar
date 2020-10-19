from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User, UserDesignation, Profile

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 'email', 'get_full_name', 'active', 'staff', 'admin',)
    list_filter = ('admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'middle_initial', 'last_name')}),
        ('Permissions', {'fields': ('admin', 'staff', 'active',)}),
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

    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Full Name'

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'designations', 'img')

    def user(self, obj):
        return obj.user.get_short_name()

    def designations(self, obj):
        return obj.designations()

admin.site.register(User, UserAdmin)
admin.site.register(UserDesignation)
