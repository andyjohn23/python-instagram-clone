from django.contrib import admin
from posts.models import Follow, Post, Stream, Tag

class PostsAdmin(admin.ModelAdmin):
    list_display = ['caption', 'image_tag', 'price', 'in_stock', 'is_active', 'created', 'updated', 'created_by']
    list_filter = ['in_stock', 'is_active']
    list_editable = ['price', 'in_stock']
    readonly_fields = ['image_tag']
    prepopulated_fields = {'slug': ('producttitle',)}

# Register your models here.
admin.site.register(Post, PostsAdmin)
admin.site.register(Follow)
admin.site.register(Stream)
admin.site.register(Tag)