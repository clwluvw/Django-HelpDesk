from django.forms import ModelForm
from tickets.models import Ticket, Comment
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError

class TicketForm(ModelForm):
    def save(self, request):
        ticket = super().save(commit=False)
        if ticket.creator is None:
            ticket.creator = request.user
        ticket.save()
        return ticket
    
    def clean(self):
        cd = self.cleaned_data

        if cd.get('creator') is not None:
            if get_user_model().objects.get(id=cd.get('creator').id).groups.filter(name='clients').exists():
                pass
            else:
                raise ValidationError("Unknown Client")
        
        return cd
    
    class Meta:
        model = Ticket
        fields = ['title', 'priority', 'creator']

class CommentForm(ModelForm):
    def save(self, request, ticket):
        comment = super().save(commit=False)
        if request.user == ticket.creator:
            ticket.state = "Waiting for response"
            comment.from_owner = True
        else:
            ticket.state = "Answered"
            comment.from_owner = False
        ticket.save()
        comment.ticket = ticket
        comment.save()
        ticket.lastUpdate = timezone.now()
        return comment

    class Meta:
        model = Comment
        fields = ['comment', 'attach']