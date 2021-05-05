from django.db import models
from posts.models import Post
from authentication.models import UserAccount
from django.utils import timezone

# Create your models here.


class Comments(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comment")
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    body = models.TextField()
    date_commented = models.DateTimeField(default=timezone.now)

    @property
    def total_comments(self):
        return self.user.all().count()
