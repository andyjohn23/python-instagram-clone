from django.contrib import admin
from messaging.models import Message

class UserMessagesAdmin(admin.ModelAdmin):
    list_display = ['user', 'sender', 'recipient', 'body', 'date', 'is_read']
    # prepopulated_fields = {'slug': ('categoryname',)}

admin.site.register(Message, UserMessagesAdmin)