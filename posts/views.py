from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import login, logout, authenticate
from .forms import NewPostForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from .models import Post, Stream, Likes, Follow
from authentication.models import Profile, UserAccount
from django.template import loader
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django.db import transaction
# Create your views here.


@login_required(login_url='index')
def PostDetail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    favourite = False

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)

        if profile.favourites.filter(id=post_id).exists():
            favourite = True

    template = loader.get_template('auth/post-detail.html')

    context = {
        'post': post,
        'favourite': favourite
    }

    return HttpResponse(template.render(context, request))


@login_required(login_url='index')
def NewPost(request):
    user = request.user.id

    if request.method == "POST":
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data.get('image')
            caption = form.cleaned_data.get('caption')

            created = Post.objects.get_or_create(
                image=image, caption=caption, user_id=user)

            return redirect('authentication:index')
    else:
        form = NewPostForm()

    return render(request, 'auth/new-posts.html')


@login_required(login_url='index')
def like(request):
    user = request.user
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    is_liked = False
    if post.liked.filter(id=user.id).exists():
        post.liked.remove(user)
        is_liked = False
    else:
        post.liked.add(user)
        is_liked = True

    return JsonResponse({'form': is_liked})


@login_required(login_url='index')
def favourites(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=user)

    if profile.favourites.filter(id=post_id).exists():
        profile.favourites.remove(post)

    else:
        profile.favourites.add(post)

    return HttpResponseRedirect(reverse('posts:postdetails', args=[post_id]))

@login_required(login_url='index')
def follow(request, option, username):
    user = request.user
    following = get_object_or_404(UserAccount, username=username)


    try:
        created = Follow.objects.get_or_create(follower=user, following=following)

        if int(option) == 0:
            created.delete()
            Stream.objects.filter(following=following, user=user).all().delete()
        else:
            posts = Post.objects.all().filter(user=following)[:5]

            with transaction.atomic():
                for post in posts:
                    Stream = Stream(post=post, user=user, date=post.posted, following=following)
                    Stream.save()
        return HttpResponseRedirect('profile', args=[username])
    except UserAccount.DoesNotExist:
        return HttpResponseRedirect('profile', args=[username])


