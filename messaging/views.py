from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='index')
def message(request):
    return render(request, 'auth/message-box.html')
