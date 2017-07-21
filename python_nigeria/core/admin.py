from django.contrib.auth import get_user_model
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from import_export.admin import ImportExportModelAdmin
from import_export import resources
from hijack_admin.admin import HijackUserAdminMixin

User = get_user_model()
admin.site.unregister(User)


class UserResource(resources.ModelResource):

    class Meta:
        model = User
        fields = ('username', 'email')
        exclude = ("date_joined", "is_active", 'password',
                   'is_staff',)


class UserAdmin(UserAdmin, ImportExportModelAdmin, HijackUserAdminMixin):
    resource_class = UserResource
    list_display = UserAdmin.list_display + (
        'hijack_field',  # Hijack button
    )

admin.site.register(User, UserAdmin)
