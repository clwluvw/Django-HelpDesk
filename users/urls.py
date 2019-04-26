from django.contrib import admin
from django.urls import include, path
from users import views

urlpatterns = [
    path('', views.Profile.as_view(), name='profile'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.RegisterView.as_view(), name='register'),
]