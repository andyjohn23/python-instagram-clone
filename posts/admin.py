from django.contrib import admin
from posts.models import Follow, Post, Stream, Tag, postExtraImages, Likes


class PostsImageInline(admin.TabularInline):
    model = postExtraImages
    extra = 3


class PostsAdmin(admin.ModelAdmin):
    list_display = ['caption', 'image_tag', 'action', 'user', 'posted', 'total_likes', 'like_count']
    # readonly_fields = ['caption', 'tags',
    #                    'image_tag', 'user', 'posted', 'likes']
    inlines = [PostsImageInline]
    # prepopulated_fields = {'slug': ('producttitle',)}


class FollowStreamAdmin(admin.ModelAdmin):
    list_display = ['following', 'user', 'post', 'date']
    readonly_fields = ['following', 'user', 'post', 'date']
    # prepopulated_fields = {'slug': ('producttitle',)}

class LikesAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'value']
    # readonly_fields = ['user', 'post', 'value']


# Register your models here.
admin.site.register(Post, PostsAdmin)
admin.site.register(Follow)
admin.site.register(Stream, FollowStreamAdmin)
admin.site.register(Likes, LikesAdmin)
admin.site.register(Tag)
