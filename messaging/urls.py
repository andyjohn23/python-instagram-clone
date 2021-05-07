from django.urls import path
from . import views

app_name = "messaging"

urlpatterns = [
    path('', views.message, name="message"),
    path('<username>/', views.directMessage, name="direct"),
]
