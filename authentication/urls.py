from django.urls import path
from . import views
from .views import userSearchResults

app_name = "authentication"

urlpatterns = [
    path('', views.login_userIndex, name="index"),
    path('login/', views.login_user, name="login"),
    path('signup/', views.register, name="signup"),
    path('search/', userSearchResults, name="search"),
    path('home/', views.home, name="home"),
    path('explore/suggested/', views.exploreSuggested, name="explore-suggested"),
    path('<uuid:post_id>/', views.commentHome, name="comment"),
    path('accounts/edit/', views.editProfile, name="settings"),
    path('accounts/password/change/', views.changePassword, name="password"),
]
