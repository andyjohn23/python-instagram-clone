from django.contrib import admin
from posts.models import Follow, Post, Stream, Tag

# Register your models here.
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Stream)
admin.site.register(Tag)