from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=254)

    def clean(self):
        cd = self.cleaned_data

        if cd.get('email') is not None:
            try:
                if get_user_model().objects.get(email=cd.get('email')):
                    raise ValidationError("This email is already exists!")
            except get_user_model().DoesNotExist:
                pass
        
        return cd

    class Meta:
        User = get_user_model()
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'remember_me')