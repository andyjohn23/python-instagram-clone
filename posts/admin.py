from django.contrib import admin
from posts.models import Follow, Post, Stream, Tag


class PostsAdmin(admin.ModelAdmin):
    list_display = ['caption', 'image_tag', 'user', 'posted', 'likes']
    readonly_fields = ['caption', 'tags', 'image', 'image_tag', 'user', 'posted', 'likes']
    # prepopulated_fields = {'slug': ('producttitle',)}


class FollowStreamAdmin(admin.ModelAdmin):
    list_display = ['following', 'user', 'post', 'date']
    readonly_fields = ['following', 'user', 'post', 'date']
    # prepopulated_fields = {'slug': ('producttitle',)}


# Register your models here.
admin.site.register(Post, PostsAdmin)
admin.site.register(Follow)
admin.site.register(Stream, FollowStreamAdmin)
admin.site.register(Tag)
