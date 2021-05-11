from django.db import models
from django.utils import timezone
import uuid
from cloudinary.models import CloudinaryField
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.conf import settings
from django.utils.html import mark_safe


class Tag(models.Model):
    title = models.CharField(max_length=75, verbose_name="tag")
    slug = models.SlugField(null=False, unique=True)

    class Meta:
        verbose_name_plural = "tags"

    def get_absolute_url(self):
        return reverse('tags', args=[self.slug])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        return super().save(*args, **kwargs)

class PostFileContent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owner")
    files = CloudinaryField('files', blank=False)

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    caption = models.TextField(max_length=1500, verbose_name="caption")
    content = models.ManyToManyField(PostFileContent, related_name="content")
    posted = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag, related_name="tag", blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    liked = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='like', default=None, blank=True)
    like_count = models.BigIntegerField(default='0')

    @property
    def total_likes(self):
        return self.liked.all().count()

    def get_absolute_url(self):
        return reverse('posts:postdetails', args=[self.id])

    def image_tag(self):
        return mark_safe('<img src="{}" width="40" height="40" />' .format(self.image.url))

    def __str__(self):
        return self.caption

    class Meta:
        ordering = ('-posted',)


LIKE_CHOICES = [
    ('like', 'like'),
    ('unlike', 'unlike'),
]


class Likes(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES,
                             default='like', max_length=10)

    def __str__(self):
        return str(self.post)

    def get_absolute_url(self):
        return reverse('postdetails', args=[self.id])


class postExtraImages(models.Model):
    post = models.ForeignKey(
        Post, related_name='postphoto', on_delete=models.CASCADE)
    image = CloudinaryField('postimage', blank=False)


class Follow(models.Model):
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following")
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="follower")
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-created',)
    
    @property
    def get_following(self):
        return self.following.all()

    @property   
    def get_following_users(self):
        following_list = [p for p in self.get_following]
        return following_list

    def __str__(self):
        return '{} follows {}'.format(self.follower, self.following)


class Stream(models.Model):
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="stream_following")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def add_post(sender, instance, *args, **kwargs):
        post = instance
        user = post.user
        followers = Follow.objects.all().filter(following=user)
        for follower in followers:
            stream = Stream(post=post, user=follower.follower,
                            date=post.posted, following=user)
            stream.save()


post_save.connect(Stream.add_post, sender=Post)
