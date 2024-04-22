from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "phone", "referral_code")
    fieldsets = (
        (
            _("Персональная информация"),
            {"fields": ("phone",)},
        ),
        (
            _("Реферальная программа"),
            {"fields": ("referral_code", "used_referral_code")},
        ),
    )
    empty_value_display = "-пусто-"
    search_fields = ("^phone",)


admin.site.unregister(Group)
