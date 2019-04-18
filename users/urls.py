from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.RegisterView.as_view(), name='signup'),
]