from django.db import models
from authentication.models import UserAccount
from django.utils import timezone

# Create your models here.


class Message(models.Model):
    user = models.ForeignKey(
        UserAccount, related_name="user", on_delete=models.CASCADE)
    sender = models.ForeignKey(
        UserAccount, related_name="sender", on_delete=models.CASCADE)
    recipient = models.ForeignKey(
        UserAccount, related_name="recipient", on_delete=models.CASCADE)
    body = models.TextField(max_length=5000, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def send_message(sender, recipient, body):
        sender_message = Message(
            user=sender, sender=sender, recipient=recipient, body=body, is_read=True)
        sender_message.save()

        recipient_message = Message(
            user=recipient, sender=sender, body=body, recipient=sender)
        recipient_message.save()

        return sender_message

    def get_message(user):
        users = []
        messages = Message.objects.filter(user=user).values(
            'recipient').annotate(last=Max('date')).order_by('-last')
        for message in messages:
            users.append({
                'user': UserAccount.objects.get(pk=message['recipient']),
                'last': message['-last'],
                'unread': Message.objects.filter(user=user, recipient__pk=message['recipient'], is_read=False).count()

            })
        return users
