from django.db import models
from django.utils import timezone
import uuid
from cloudinary.models import CloudinaryField
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.conf import settings
from django.utils.html import mark_safe
from .utils import get_filtered_image


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


ACTION_CHOICES = (
    ('NO_FILTER', 'no filter'),
    ('COLORIZED', 'colorized'),
    ('GRAYSCALE', 'grayscale'),
    ('BLURRED', 'blurred'),
    ('BINARY', 'binary'),
    ('INVERT', 'invert')
)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    caption = models.TextField(max_length=1500, verbose_name="caption")
    image = CloudinaryField('post-image', blank=False)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
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

        def save(self, *args, **kwargs):

            pil_img = Image.open(self.image)

            #  convert image to an array for processing
            cv_img = np.array(pil_img)
            img = get_filtered_image(cv_img, self.action)

            #  convert back to image
            img_pil = Image.fromarray(img)

            #  saving
            buffer = BytesIO()
            img_pil.save(buffer, format='png')
            image_png = buffer.getvalue()

            self.image.save(str(self.image), ContentFile(
                image_png), save=False)

            super().save(*args, **kwargs)

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
