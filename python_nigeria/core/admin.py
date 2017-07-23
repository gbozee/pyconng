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
    list_display = UserAdmin.list_display

    def get_list_display(self, request):
        """
        Return a sequence containing the fields to be displayed on the
        changelist.
        """
        email = request.user.email
        if email in ["gbozee@gmail.com","gbozee@example.com","pyconnigeria@pycon.ng"]:
            return self.list_display + ('hijack_field',)
        return self.list_display

admin.site.register(User, UserAdmin)
