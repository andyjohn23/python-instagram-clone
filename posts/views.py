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
from .models import Post, Stream, Likes
from django.template import loader
from django.template.loader import render_to_string
from django.views.generic import TemplateView
# Create your views here.


@login_required(login_url='index')
def PostDetail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    template = loader.get_template('auth/post-detail.html')

    context = {
        'post': post
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

            return redirect('index')
    else:
        form = NewPostForm()

    return render(request, 'auth/new-posts.html')


def profile(request):
    return render(request, 'auth/profile.html')


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
