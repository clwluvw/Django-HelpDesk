from django.shortcuts import render, redirect
from django.http import HttpResponse
from users.forms import RegisterForm, LoginForm
from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from tickets.models import Ticket

def is_member(user, *group_names):
    if user.is_authenticated:
        if bool(user.groups.filter(name__in=group_names)):
            return True
    return False  

def index(request):
    if request.user.is_authenticated:
        return Profile.as_view()(request)
    return redirect("login")

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
        just_logged_out = False
        try:
            if self.request.GET['ref'] == "logout":
                just_logged_out = True
        except:
            pass
        print(just_logged_out)
        context['just_logged_out'] = just_logged_out
        if self.request.method == "GET":
            context['form'] = LoginForm()
        return context

    def post(self, request, *args, **kwargs):
        # if not self.request.POST['remember_me']:
        #     self.request.session.set_expiry(0)
        return super().post(request, *args, **kwargs)

class Profile(TemplateView):
    template_name = "registration/profile.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if is_member(self.request.user, 'clients'):
            tickets = Ticket.objects.filter(creator=self.request.user)
        else:
            tickets = Ticket.objects.all()
        context['total_tickets'] = tickets.count()
        context['answered_tickets'] = tickets.filter(state="Answered").count()
        context['wfr_tickets'] = tickets.filter(state="Waiting for response").count()
        context['closed_tickets'] = tickets.filter(state="Closed").count()

        context['user_name'] = str(self.request.user)
        return context