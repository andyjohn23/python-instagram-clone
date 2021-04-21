from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'auth/index.html')

def login(request):
    return render(request, 'auth/login-page.html')

def signUp(request):
    return render(request, 'auth/register-page.html')
