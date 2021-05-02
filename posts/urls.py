from django.urls import path
from . import views

urlpatterns = [
    path('newpost/', views.NewPost, name='newpost'),
    path('<uuid:post_id>/', views.PostDetail, name="postdetails"),
    path('profile/', views.profile, name="profile"),
    path('like/', views.like, name="postlike"),
]
