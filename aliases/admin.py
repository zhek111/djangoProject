from django.contrib import admin
from django.contrib.admin import display
from django.urls import reverse
from django.utils.safestring import mark_safe

from aliases.models import Alias


class AliasAdmin(admin.ModelAdmin):
    list_display_links = ('first_name', )
    list_display = ('first_name', 'last_name', 'user_link', 'approved')
    readonly_fields = ('full_name', 'aliases')
    fieldsets = (
        ('User', {'fields': (
            'user', 'full_name', 'aliases')}),
        ('Alias', {'fields': (
            'first_name', 'last_name', 'approved')}),
    )

    @display(description='User')
    def user_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:users_customuser_change", args=(obj.user.pk,)),
            obj.user.email
        ))

    def full_name(self, obj):
        return obj.user.full_name

    def aliases(self, obj):
        aliases = Alias.objects.filter(user=obj.user).exclude(id=obj.id)
        return '\n'.join([f'{alias.first_name} {alias.last_name}' for alias in aliases])

admin.site.register(Alias, AliasAdmin)
