from django.db import models
from authentication.models import UserAccount
from django.utils import timezone

# Create your models here.

class Message(models.Model):
    user = models.ForeignKey(UserAccount, related_name="user", on_delete=models.CASCADE)
    sender = models.ForeignKey(UserAccount, related_name="sender", on_delete=models.CASCADE)
    recipient = models.ForeignKey(UserAccount, related_name="recipient", on_delete=models.CASCADE)
    body = models.TextField(max_length=5000, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def send_message(sender, recipient, body):
        sender_message = Message(user=sender, sender=sender, recipient=recipient, body=body, is_read=True)
        sender_message.save()


