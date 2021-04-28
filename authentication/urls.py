from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_userIndex, name="index"),
    path('login/', views.login_user, name="login"),
    path('signup/', views.register, name="signup"),
    path('home/', views.home, name="home"),
    path('newpost/', views.NewPost, name='newpost'),
    path('<uuid:post_id>/', views.PostDetail, name="postdetails"),
    path('profile/', views.profile, name="profile")
]
