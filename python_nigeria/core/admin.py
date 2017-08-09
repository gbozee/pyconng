from django.contrib.auth import get_user_model
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from import_export.admin import ImportExportModelAdmin
from import_export import resources
from hijack_admin.admin import HijackUserAdminMixin
from symposion.sponsorship.admin import SponsorAdmin
from .models import Sponsor, SponsorImage
User = get_user_model()
admin.site.unregister(User)
admin.site.unregister(Sponsor)


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
        if email in ["gbozee@gmail.com", "gbozee@example.com", "pyconnigeria@pycon.ng"]:
            return self.list_display + ('hijack_field',)
        return self.list_display


admin.site.register(User, UserAdmin)


class SponsorImageInline(admin.TabularInline):
    model = SponsorImage


class NewSponorAdmin(SponsorAdmin):
    inlines = SponsorAdmin.inlines + [SponsorImageInline]
    list_display = SponsorAdmin.list_display + ['image']

    def get_queryset(self, request):
        query = super().get_queryset(request)
        return query.select_related('image_link')

    def image(self, obj):
        if hasattr(obj, "image_link"):
            return '<img src="{}" alt="image" />'.format(
                obj.image_link.image.url)

    image.allow_tags = True


admin.site.register(Sponsor, NewSponorAdmin)
