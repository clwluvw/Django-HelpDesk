from django.contrib import admin
from tickets.models import Ticket, Comment

admin.site.register(Ticket)
admin.site.register(Comment)
