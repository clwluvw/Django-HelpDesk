from django.contrib import admin
from django.urls import include, path
from users import views

urlpatterns = [
    path('login/', views.SigninView.as_view(), name='login'),
    path('', include('django.contrib.auth.urls')),
    path('register/', views.RegisterView.as_view(), name='register'),
]