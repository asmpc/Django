from django.contrib import admin
from account.models import User




class UserAdmin(admin.ModelAdmin):
    exclude = ('groups', 'user_permissions',)
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff',)
    list_display_links = ('email', 'username',)
    list_editable = ('first_name', 'last_name', 'is_staff',)
    list_filter = ('is_staff', 'is_superuser',)




admin.site.register(User, UserAdmin)

# Register your models here.
