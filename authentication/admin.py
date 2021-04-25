from django.contrib import admin
from authentication.models import UserAccount, Profile

class UserAccountAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'created', 'is_active', 'is_admin', 'is_superuser', 'is_staff']
    # prepopulated_fields = {'slug': ('categoryname',)}

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'image', 'url', 'get_favourites', 'description', 'created', 'last_login']
    # prepopulated_fields = {'slug': ('categoryname',)}

# Register your models here.
admin.site.register(UserAccount, UserAccountAdmin)
admin.site.register(Profile, UserProfileAdmin)
