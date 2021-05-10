from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterUserForm, AuthenticationForm, ProfileUpdateForm, UserUpdateForm
from posts.forms import NewPostForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from .models import UserAccount, Profile
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from posts.models import Post, Stream, Likes, Follow
from django.template import loader
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django.urls import resolve
from comments.models import Comments
from comments.forms import commentForm
# from django.views.generic import CreateView
# from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Create your views here.


@login_required(login_url='authentication:index')
def userProfile(request, username):
    user = get_object_or_404(UserAccount, username=username)
    profile = Profile.objects.get(user=user)
    url_name = resolve(request.path).url_name
    title = profile

    if url_name == 'profile':
        posts = Post.objects.filter(user=user).order_by('-posted')

    else:
        posts = profile.favourites.all()

    number_of_post = Post.objects.filter(user=user).count()
    number_of_following = Follow.objects.filter(follower=user).count()
    number_of_followers = Follow.objects.filter(following=user).count()

    follow_status = Follow.objects.filter(
        following=user, follower=request.user).exists()

    template = loader.get_template('auth/profile.html')

    context = {
        'posts': posts,
        'profile': profile,
        'url_name': url_name,
        'number_of_post': number_of_post,
        'number_of_following': number_of_following,
        'number_of_followers': number_of_followers,
        'follow_status': follow_status,
        'title': title
    }

    return HttpResponse(template.render(context, request))


@login_required(login_url='authentication:index')
def home(request):
    user = request.user
    suggest_users = Profile.objects.all().exclude(user=user)
    follow_status = Follow.objects.filter(
        following=user, follower=request.user).exists()
    posts = Stream.objects.filter(user=user)

    group_ids = []

    for post in posts:
        group_ids.append(post.post_id)

    post_items = Post.objects.filter(
        id__in=group_ids).all().order_by('-posted')

    template = loader.get_template('auth/home.html')
    context = {
        'post_items': post_items,
        'suggest_users': suggest_users,
        'follow_status': follow_status
    }

    return HttpResponse(template.render(context, request))


def register(request, *arg, **kwargs):
    user = request.user

    if user.is_authenticated:
        return redirect('authentication:home')
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
            return redirect('authentication:home')
        else:
            context['register_form'] = form

    return render(request, 'auth/register-page.html', context)


def logout_user(request, *args, **kwargs):
    logout(request)
    return redirect("authentication:index")


def login_user(request, *args, **kwargs):

    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('authentication:home')

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
                return redirect('authentication:home')

        else:
            context['login_form'] = form

    return render(request, 'auth/login-page.html', context)


def login_userIndex(request, *args, **kwargs):

    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('authentication:home')

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
                return redirect('authentication:home')

        else:
            context['login_form'] = form

    return render(request, 'auth/index.html', context)


def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get('next'):
            redirect = str(request.GET.get('next'))

    return redirect


@login_required(login_url='authentication:index')
def editProfile(request):

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Profile updated successfully')
            return redirect('authentication:settings')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'auth/edit-profile.html', context)


@login_required(login_url='authentication:index')
def commentHome(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)

    comments = Comments.objects.filter(post=post).order_by('date_commented')

    if request.method == 'POST':
        form = commentForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data.get('body')
            body = form.save(commit=False)
            body.post = post
            body.user = user
            body.save()

            return HttpResponseRedirect(reverse('authentication:home', args=[post_id]))
    else:
        form = commentForm(request.POST)

    template = loader.get_template('auth/home.html')
    context = {
        'comments': comments,
        'form': form
    }

    return HttpResponse(template.render(context, request))


@login_required(login_url='authentication:index')
def changePassword(request):
    return render(request, 'auth/change-password.html')

