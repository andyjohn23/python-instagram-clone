from django.urls import path
from . import views
from .views import PostListView

urlpatterns = [
    path('', views.login_userIndex, name="index"),
    path('login/', views.login_user, name="login"),
    path('signup/', views.register, name="signup"),
    path('home/', PostListView.as_view(), name="home"),
]
