from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=254)

    class Meta:
        User = get_user_model()
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')