from django.shortcuts import render, redirect
from django.http import HttpResponse
from users.forms import RegisterForm
from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView

class RegisterView(TemplateView):
    template_name = "users/register.html"

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']            
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/accounts/profile')
        return render(request, 'users/register.html', {'form':form})