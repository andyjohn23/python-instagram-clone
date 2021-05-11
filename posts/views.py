from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import login, logout, authenticate
from .forms import NewPostForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, UpdateView
from .models import Post, Stream, Likes, Follow, PostFileContent
from authentication.models import Profile, UserAccount
from django.template import loader
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django.db import transaction
from comments.models import Comments
from comments.forms import commentForm
from django.template import RequestContext
# Create your views here.


@login_required(login_url='authentication:index')
def PostDetail(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    favourite = False

    comments = Comments.objects.filter(post=post).order_by('date_commented')

    if request.method == 'POST':
        form = commentForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data.get('body')
            body = form.save(commit=False)
            body.post = post
            body.user = user
            body.save()

            return HttpResponseRedirect(reverse('posts:postdetails', args=[post_id]))
    else:
        form = commentForm(request.POST)

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)

        if profile.favourites.filter(id=post_id).exists():
            favourite = True

    template = loader.get_template('auth/post-detail.html')

    context = {
        'post': post,
        'favourite': favourite,
        'form': form,
        'comments': comments
    }

    return HttpResponse(template.render(context, request))


@login_required(login_url='authentication:index')
def NewPost(request):
    user = request.user
    file_image = []

    if request.method == "POST":
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            content = request.FILES.getlist('content')
            caption = form.cleaned_data.get('caption')

            for files in content:
                file_instance = PostFileContent(files=files, user=user)
                file_instance.save()
                file_image.append(file_instance)


            p, created = Post.objects.get_or_create(
                caption=caption, user=user)
            p.content.set(file_image)
            p.save()
            
            messages.success(
                request, f'Post uploaded successfully see in profile')
            return redirect('posts:newpost')
    else:
        form = NewPostForm()
    
    context = {
        'form': form
    }

    return render(request, 'auth/new-posts.html', context)


@login_required(login_url='authentication:index')
def like(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)

        else:
            post_obj.liked.add(user)

            like, created = Likes.objects.get_or_create(
                user=user, post_id=post_id)

            if not created:
                if like.value == 'like':
                    like.value == 'unlike'
                else:
                    like.value == 'like'
                post_obj.save()
                like.save()

                # data = {
                #     'value': like.value,
                #     'likes': post_obj.liked.all().count()
                # }
                # return JsonResponse(data, safe=False)

        return redirect('authentication:home')

@login_required(login_url='authentication:index')
def detail_like(request, post_id):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)

        else:
            post_obj.liked.add(user)

            like, created = Likes.objects.get_or_create(
                user=user, post_id=post_id)

            if not created:
                if like.value == 'like':
                    like.value == 'unlike'
                else:
                    like.value == 'like'
                post_obj.save()
                like.save()

                # data = {
                #     'value': like.value,
                #     'likes': post_obj.liked.all().count()
                # }
                # return JsonResponse(data, safe=False)

        return redirect('posts:postdetails', args=[post_id])

@login_required(login_url='authentication:index')
def favourites(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=user)

    if profile.favourites.filter(id=post_id).exists():
        profile.favourites.remove(post)

    else:
        profile.favourites.add(post)

    return HttpResponseRedirect(reverse('posts:postdetails', args=[post_id]))


@login_required(login_url='authentication:index')
def follow(request, option, username):
    user = request.user
    following = get_object_or_404(UserAccount, username=username)

    try:
        p, created = Follow.objects.get_or_create(
            follower=user, following=following)

        if int(option) == 0:
            p.delete()
            Stream.objects.filter(following=following,
                                  user=user).all().delete()
        else:
            posts = Post.objects.all().filter(user=following)[:3]

            with transaction.atomic():
                for post in posts:
                    stream = Stream(post=post, user=user,
                                    date=post.posted, following=following)
                    stream.save()
        return HttpResponseRedirect(reverse('profile', args=[username]))
    except UserAccount.DoesNotExist:
        return HttpResponseRedirect(reverse('profile', args=[username]))


@login_required(login_url='authentication:index')
def updatePostView(request, post_id):
    user = request.user.id
    post = Post.objects.get(id=post_id, user_id=user)
    post_form = NewPostForm(instance=post, data=request.POST)
    if post_form.is_valid():
        post_form.save()
        return HttpResponseRedirect(reverse('posts:postedit'))
    else:
        post = Post.objects.get(pk=post_id, user_id=user)
        post_form = NewPostForm(instance=post)
    return render(request, 'auth/update_post.html', {'form': post_form})
