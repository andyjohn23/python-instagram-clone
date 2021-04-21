from django.contrib import admin
from authentication.models import UserAccount, Profile

# Register your models here.
admin.site.register(UserAccount)
admin.site.register(Profile)
