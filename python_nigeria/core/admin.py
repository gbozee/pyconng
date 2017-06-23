from django.contrib.auth import get_user_model
from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from import_export import resources

User = get_user_model()
admin.site.unregister(User)

class UserResource(resources.ModelResource):

    class Meta:
        model = User


class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource

admin.site.register(User, UserAdmin)