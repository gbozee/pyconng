from django.contrib.auth import get_user_model
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from import_export.admin import ImportExportModelAdmin
from import_export import resources
from hijack_admin.admin import HijackUserAdminMixin
from symposion.sponsorship.admin import SponsorAdmin
from .models import Sponsor, SponsorImage
from symposion.proposals.models import ProposalSection
from django.contrib.auth.models import Permission
from symposion.speakers.models import Speaker
from symposion.reviews.models import ProposalResult

User = get_user_model()
admin.site.unregister(User)
admin.site.unregister(Sponsor)
admin.site.unregister(Speaker)
admin.site.unregister(ProposalResult)


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ["name", "pk", "email", "created", "twitter_username"]
    search_fields = ["name"]


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ("username", "email")
        exclude = ("date_joined", "is_active", "password", "is_staff")


class ProposalResultResource(resources.ModelResource):
    class Meta:
        model = ProposalResult
        fields = (
            "pk",
            "proposal__id",
            "proposal__title",
            "proposal__kind__name",
            "status",
            "score",
            "vote_count",
            "accepted",
            "plus_one",
            "plus_zero",
            "minus_zero",
            "minus_one",
        )


class TwitterProposalResource(resources.ModelResource):
    talk_title = resources.Field()
    speaker = resources.Field()
    photo = resources.Field()

    class Meta:
        model = ProposalResult
        fields = ("talk_title", "speaker","proposal__speaker__twitter_username", "photo", )

    def dehydrate_talk_title(self, book):
        return book.proposal.title

    def get_speaker(self, obj):
        return obj.proposal.speaker

    def dehydrate_speaker(self, book):
        speaker = self.get_speaker(book)
        return speaker.name

    def dehydrate_photo(self, book):
        speaker = self.get_speaker(book)
        if speaker.photo:
            return speaker.photo.url




@admin.register(ProposalResult)
class ProposalResultAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = TwitterProposalResource
    # resource_class = ProposalResultResource
    list_display = ["proposal", "status", "score", "vote_count", "accepted", "pk"]
    list_filter = ["proposal__kind__name", "status"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("proposal__speaker")


class UserAdmin(UserAdmin, ImportExportModelAdmin, HijackUserAdminMixin):
    resource_class = UserResource
    list_display = UserAdmin.list_display
    actions = ["remove_permission"]

    def get_list_display(self, request):
        """
        Return a sequence containing the fields to be displayed on the
        changelist.
        """
        email = request.user.email
        if email in ["gbozee@gmail.com", "gbozee@example.com", "pyconnigeria@pycon.ng"]:
            return self.list_display + ("hijack_field",)
        return self.list_display

    def remove_permission(self, request, queryset):
        permissions = Permission.objects.filter(codename__icontains="add_review")

        for x in queryset.all():
            x.user_permissions.remove(*permissions)
        self.message_user(request, "permissions added")


admin.site.register(User, UserAdmin)


class SponsorImageInline(admin.TabularInline):
    model = SponsorImage


class NewSponorAdmin(SponsorAdmin):
    inlines = SponsorAdmin.inlines + [SponsorImageInline]
    list_display = SponsorAdmin.list_display + ["image"]

    def get_queryset(self, request):
        query = super().get_queryset(request)
        return query.select_related("image_link")

    def image(self, obj):
        if hasattr(obj, "image_link"):
            return '<img src="{}" alt="image" />'.format(obj.image_link.image.url)

    image.allow_tags = True


admin.site.register(Sponsor, NewSponorAdmin)
