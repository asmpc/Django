from django.contrib import admin
from account.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin



# class UserAdmin(admin.ModelAdmin):
class UserAdmin(BaseUserAdmin):
    readonly_fields = ("date_joined",)
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff',)
    list_display_links = ('email', 'username',)
    list_editable = ('first_name', 'last_name', 'is_staff',)
    list_filter = ('is_staff', 'is_superuser',)




admin.site.register(User, UserAdmin)


