from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from .models import Ticket


@login_required
def ticket_list(request):
    return render(request, "ticket_list.html")


@login_required
def get_tickets(request):
    tickets = Ticket.objects.all()
    return render(request, "_tickets.html", {"tickets": tickets})


@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, "ticket_detail.html", {"ticket": ticket})


@login_required
@require_POST
def submit_ticket(request):
    title = request.POST["title"]
    ticket = Ticket.objects.create(title=title, user=request.user)
    return render(request, "_ticket.html", {"ticket": ticket})
