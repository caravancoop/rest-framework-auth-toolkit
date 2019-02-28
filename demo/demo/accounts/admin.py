from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin

from rest_auth_toolkit.admin import BaseEmailUserAdmin

from .models import APIToken, BaseGroup, Group, User, EmailConfirmation


class UserAdmin(BaseEmailUserAdmin):
    date_hierarchy = 'date_joined'
    readonly_fields = ('date_joined', 'last_login')


class EmailConfirmationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'confirmed')
    date_hierarchy = 'created'
    readonly_fields = ('external_id', 'created', 'modified')


class APITokenAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created')
    ordering = ('user', '-created')
    date_hierarchy = 'created'
    readonly_fields = ('key', 'created')


admin.site.register(User, UserAdmin)
admin.site.unregister(BaseGroup)
admin.site.register(Group, GroupAdmin)
admin.site.register(EmailConfirmation, EmailConfirmationAdmin)
admin.site.register(APIToken, APITokenAdmin)
