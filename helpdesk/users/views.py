from django.shortcuts import render, redirect
from django.http import HttpResponse
from users.forms import RegisterForm, LoginForm
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from tickets.models import Ticket
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone
from django.contrib.auth.models import Group

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

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("profile")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            clients = Group.objects.get(name="clients")
            clients.user_set.add(user)
            if not form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0)
            return redirect('/accounts/profile')
        return render(request, 'registration/register.html', {'form':form})

class SigninView(LoginView):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("profile")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        just_logged_out = False
        try:
            if self.request.GET['ref'] == "logout":
                just_logged_out = True
        except:
            pass
        context['just_logged_out'] = just_logged_out
        if self.request.method == "GET":
            context['form'] = LoginForm()
        return context

    def post(self, request, *args, **kwargs):
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)
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
        context['user_name'] = str(self.request.user)

        context['total_tickets'] = {}
        context['total_tickets']['count'] = tickets.filter(dateTime__year = timezone.now().year).count()
        context['total_tickets']['months'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(1, 13):
            context['total_tickets']['months'][i-1] = tickets.filter(dateTime__month = i,
                                                                        dateTime__year = timezone.now().year).count()

        context['answered_tickets'] = {}
        context['answered_tickets']['count'] = tickets.filter(state="Answered",
                                                                dateTime__year = timezone.now().year).count()
        context['answered_tickets']['months'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(1, 13):
            context['answered_tickets']['months'][i-1] = tickets.filter(state="Answered",
                                                                            dateTime__month = i,
                                                                            dateTime__year = timezone.now().year).count()

        context['wfr_tickets'] = {}
        context['wfr_tickets']['count'] = tickets.filter(state="Waiting for response",
                                                            dateTime__year = timezone.now().year).count()
        context['wfr_tickets']['months'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(1, 13):
            context['wfr_tickets']['months'][i-1] = tickets.filter(state="Waiting for response",
                                                                    dateTime__month = i,
                                                                    dateTime__year = timezone.now().year).count()

        context['closed_tickets'] = {}
        context['closed_tickets']['count'] = tickets.filter(state="Closed",
                                                            dateTime__year = timezone.now().year).count()
        context['closed_tickets']['months'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(1, 13):
            context['closed_tickets']['months'][i-1] = tickets.filter(state="Closed",
                                                                        dateTime__month = i,
                                                                        dateTime__year = timezone.now().year).count()

        context['all_tickets'] = tickets.count()
        context['tickets_statistics'] = [
            tickets.filter(state="Answered").count(),
            tickets.filter(state="Waiting for response").count(),
            tickets.filter(state="Closed").count()
        ]
        
        return context

class UserProfile(TemplateView):
    template_name = "registration/user-profile.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            context = self.get_context_data(**kwargs)
            context['message'] = "Your password was successfully updated!"
            context['form'] = PasswordChangeForm
            return render(request, self.template_name, context)
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PasswordChangeForm(self.request.user)
        context['username'] = self.request.user.username
        context['user_name'] = str(self.request.user)
        context['email'] = self.request.user.email
        return context

def redirectToProfile(request):
    return redirect("profile")