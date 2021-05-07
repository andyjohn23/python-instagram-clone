from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Message

# Create your views here.


@login_required(login_url='index')
def message(request):
    user = request.user
    messages = Message.get_messages(user=user)
    active_user = None
    directs = None

    if messages:
        message = messages[0]
        active_user = message['user'].username
        directs = Message.objects.filter(user=user, recipient=message['user'])
        directs.update(is_read=True)

        for message in messages:
            if message['user'].username == active_user:
                message['unread'] = 0

        context = {
            'messages': messages,
            'directs': directs,
            'active_user': active_user
        }

    template = loader.get_template('auth/message-box.html')

    return HttpResponse(template.render(context, request))
