from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin as BaseUserAdmin

from .models import APIToken, BaseGroup, Group, User, EmailConfirmation


class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    add_form_template = None
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    date_hierarchy = 'date_joined'
    readonly_fields = ('username', 'date_joined', 'last_login')


class EmailConfirmationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'confirmed')
    date_hierarchy = 'created'
    readonly_fields = ('external_id', 'created', 'modified')


class APITokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'created')
    ordering = ('user', '-created')
    date_hierarchy = 'created'
    readonly_fields = ('key', 'created')


admin.site.register(User, UserAdmin)
admin.site.unregister(BaseGroup)
admin.site.register(Group, GroupAdmin)
admin.site.register(EmailConfirmation, EmailConfirmationAdmin)
admin.site.register(APIToken, APITokenAdmin)
