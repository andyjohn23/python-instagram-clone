from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from .models import Message
from django.template import loader
from authentication.models import UserAccount

# Create your views here.


@login_required(login_url='authentication:index')
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

    template = loader.get_template('auth/message-box.html')

    context = {
        'messages': messages,
        'directs': directs,
        'active_user': active_user
    }

    return HttpResponse(template.render(context, request))


@login_required(login_url='authentication:index')
def directMessage(request, username):
    user = request.user
    messages = Message.get_messages(user=user)
    active_user = username
    directs = Message.objects.filter(user=user, recipient__username=username)
    directs.update(is_read=True)

    for message in messages:
        if message['user'].username == username:
            message['unread'] = 0

    template = loader.get_template('auth/message-box.html')

    context = {
        'messages': messages,
        'directs': directs,
        'active_user': active_user
    }

    return HttpResponse(template.render(context, request))

@login_required(login_url='authentication:index')
def sendDirect(request):
    sender = request.user
    recipient = request.POST.get('to_user')
    body = request.POST.get('body')

    if request.method == 'POST':
        to_user = UserAccount.objects.get(username=recipient)
        Message.get_messages(sender, to_user, body)

        return redirect('messaging:message')
    else:
        return HttpResponseBadRequest()
