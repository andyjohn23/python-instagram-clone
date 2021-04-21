from django.db import models
from django.utils import timezone
import uuid
from cloudinary.models import CloudinaryField
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.conf import settings


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


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    caption = models.TextField(max_length=1500, verbose_name="caption")
    image = CloudinaryField('post-image', blank=False)
    posted = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag, related_name="tag")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    likes = models.IntegerField()

    def get_absolute_url(self):
        return reverse('postdetails', args=[self.slug])

    def __str__(self):
        return self.caption


class Follow(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following")


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
