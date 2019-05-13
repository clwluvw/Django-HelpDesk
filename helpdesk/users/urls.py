from django.contrib import admin
from django.urls import include, path
from users import views

urlpatterns = [
    path('', views.index, name='profile'),
    path('accounts/login/', views.SigninView.as_view(), name='login'),
    path('accounts/edit/', views.UserProfile.as_view(), name='edit profile'),
    path('accounts/profile/', views.redirectToProfile),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.RegisterView.as_view(), name='register'),
]