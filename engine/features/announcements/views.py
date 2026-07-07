from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Announcement
from features.injects.models import Inject, InjectSubmission
from features.teams.models import Team

# Create your views here.
@login_required
def dashboard(request):
  try:
    team = Team.objects.get(user=request.user)
  except Team.DoesNotExist:
    return redirect("admin:index")
  
  announcements = Announcement.objects.order_by("-published_at")[:5]
  injects = list(Inject.objects.order_by("start_time"))

  submitted_ids = set(InjectSubmission.objects.filter(team=team, submitted_at__isnull=False).values_list("inject_id", flat=True))
  for inject in injects:
    inject.is_submitted = inject.id in submitted_ids

  return render(request, "dashboard.html", {
    "team": team,
    "announcements": announcements,
    "injects": injects,
  })
