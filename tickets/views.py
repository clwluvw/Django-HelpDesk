from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from tickets.forms import TicketForm, CommentForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from tickets.models import Ticket, Comment
from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import Http404

def is_member(user, *group_names):
    if user.is_authenticated:
        if bool(user.groups.filter(name__in=group_names)) or user.is_superuser:
            return True
    return False   

class NewTicket(TemplateView):
    template_name = "tickets/add-ticket.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ticketForm'] = TicketForm()
        context['commentForm'] = CommentForm()
        context['is_support'] = is_member(self.request.user, 'supports')
        if (context['is_support']):
            context['clients'] = []
            context['clients'] = get_user_model().objects.filter(groups__name='clients')
        context['user_name'] = str(self.request.user)
        return context
    
    def post(self, request):
        ticketForm = TicketForm(request.POST)
        commentForm = CommentForm(request.POST)

        if ticketForm.is_valid() and commentForm.is_valid():
            ticket = ticketForm.save(request)
            comment = commentForm.save(request, ticket)
            return redirect('ticket details', ticket_id=ticket.id)
        context = self.get_context_data()
        context['ticketForm'] = ticketForm
        context['commentForm'] = commentForm
        return render(request, 'tickets/add-ticket.html', context)

class TicketsList(ListView):
    model = Ticket
    template_name = "tickets/tickets-list.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.has_perm('users.support'):
            return Ticket.objects.all()
        elif self.request.user.has_perm('users.client'):
            return Ticket.objects.filter(creator=self.request.user)
        return []
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_support'] = self.request.user.has_perm('users.support')
        context['user_name'] = str(self.request.user)
        return context

class TicketDetails(ListView):
    template_name = "tickets/ticket.html"
    context_object_name = "comments"
    model = Comment
    paginate_by = 10

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or Ticket.objects.filter(creator=request.user, id=kwargs['ticket_id']):
            return super().dispatch(request, *args, **kwargs)
        raise Http404
    
    def get_queryset(self):
        return Comment.objects.filter(ticket=self.kwargs['ticket_id']).order_by('-dateTime')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['commentForm'] = CommentForm()
        context['ticket'] = Ticket.objects.get(id=self.kwargs['ticket_id'])
        context['user_name'] = str(self.request.user)
        return context
    
    def post(self, request, *args, **kwargs):
        commentForm = CommentForm(request.POST)
        if commentForm.is_valid():
            commentForm.save(request, Ticket.objects.get(id=kwargs['ticket_id']))
            return self.get(request, kwargs)
        context = self.get_context_data() #check for error on empty message
        context['commentForm'] = commentForm
        return render(request, template_name, context)
    
    def get(self, request, *args, **kwargs):
        close_state = request.GET.get('close', None)
        if close_state is not None and close_state == "true":
            ticket = Ticket.objects.get(id=kwargs['ticket_id'])
            ticket.state = "Closed"
            ticket.save()
            return redirect("tickets list")
        return super().get(request, *args, **kwargs)