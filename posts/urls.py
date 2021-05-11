from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path('newpost/', views.NewPost, name='newpost'),
    path('<uuid:post_id>/', views.PostDetail, name="postdetails"),
    path('<uuid:post_id>/edit/', views.updatePostView, name="postedit"),
    path('like/', views.like, name="postlike"),
    path('like/', views.detail_like, name="detail-like"),
    path('<uuid:post_id>/savedpost', views.favourites, name="postfavourite"),
]
