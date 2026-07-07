from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Service

# Create your views here.
@login_required
def services(request):
  all_services = Service.objects.select_related("team").order_by("team__name", "service_name")
  service_types = sorted(set(service.service_name for service in all_services))
  teams = {}

  for service in all_services:
    teams.setdefault(service.team.name, {})[service.service_name] = service.is_up

  grid = []
  for team_name, statuses in teams.items():
    statuses_list = []
    for service_type in service_types:
      statuses_list.append(statuses.get(service_type))
    grid.append({"team": team_name, "statuses": statuses_list})

  return render(request, "services.html", {"service_types": service_types, "grid": grid,})
