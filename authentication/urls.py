from django.urls import path
from . import views

app_name = "authentication"

urlpatterns = [
    path('', views.login_userIndex, name="index"),
    path('login/', views.login_user, name="login"),
    path('signup/', views.register, name="signup"),
    path('home/', views.home, name="home"),
]
