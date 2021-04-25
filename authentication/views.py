from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterUserForm, AuthenticationForm
from posts.forms import NewPostForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from .models import UserAccount, Profile
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from posts.models import Post, Stream
from django.template import loader
# from django.views.generic import CreateView
# from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# from .forms import ProjectSearchForm, RatesForm
# from .serializer import userSerializer, projectSerializer
# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.response import Response

# Create your views here.


@login_required(login_url='index')
def home(request):
    user = request.user
    posts = Stream.objects.filter(user=user)

    group_ids = []

    for post in posts:
        group_ids.append(post.post_id)

    post_items = Post.objects.filter(
        id__in=group_ids).all().order_by('-posted')

    template = loader.get_template('auth/home.html')
    context = {
        'post_items': post_items
    }

    return HttpResponse(template.render(context, request))


def register(request, *arg, **kwargs):
    user = request.user

    if user.is_authenticated:
        return redirect('home')
    context = {}

    if request.POST:
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            destination = get_redirect_if_exists(request)
            if destination:
                return redirect(destination)
            return redirect('home')
        else:
            context['register_form'] = form

    return render(request, 'auth/register-page.html', context)


def logout_user(request, *args, **kwargs):
    logout(request)
    return redirect("index")


def login_user(request, *args, **kwargs):

    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('home')

    destination = get_redirect_if_exists(request)
    if request.POST:
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                destination = get_redirect_if_exists(request)
                if destination:
                    return redirect(destination)
                return redirect('home')

        else:
            context['login_form'] = form

    return render(request, 'auth/login-page.html', context)


def login_userIndex(request, *args, **kwargs):

    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('home')

    destination = get_redirect_if_exists(request)
    if request.POST:
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                destination = get_redirect_if_exists(request)
                if destination:
                    return redirect(destination)
                return redirect('home')

        else:
            context['login_form'] = form

    return render(request, 'auth/index.html', context)


def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get('next'):
            redirect = str(request.GET.get('next'))

    return redirect


@login_required(login_url='index')
def PostDetail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    template = loader.get_template('post-detail.html')

    context = {
        'post': post,
    }

    return HttpResponse(template.render(request, context))


@login_required(login_url='index')
def NewPost(request):
    user = request.user.id

    if request.method == "POST":
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data.get('image')
            caption = form.cleaned_data.get('caption')

            p, created = Post.objects.get_or_create(
                image=image, caption=caption, user_id=user)
            p.save()
            return redirect('index')
    else:
        form = NewPostForm()

    context = {
        'form': form
    }

    return render(request, 'auth/new-posts.html', context)
