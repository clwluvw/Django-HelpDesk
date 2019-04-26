from django.shortcuts import render, redirect
from django.http import HttpResponse
from users.forms import *
from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView

class RegisterView(TemplateView):
    template_name = "registration/register.html"

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']            
            user = authenticate(username=username, password=password)
            login(request, user)
            if not form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0)
            return redirect('/accounts/profile')
        return render(request, 'registration/register.html', {'form':form})

class SigninView(LoginView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == "GET":
            context['form'] = LoginForm()
        return context

    def post(self, request, *args, **kwargs):
        # if not self.request.POST['remember_me']:
        #     self.request.session.set_expiry(0)
        return super().post(request, *args, **kwargs)