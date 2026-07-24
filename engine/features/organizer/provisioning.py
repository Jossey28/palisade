from django.contrib.auth.models import User
from features.teams.models import Team


def provision_teams(competition, num_teams, username_prefix, default_password):
  """Create real User + Team rows for a competition. This is the working part
  of provisioning - accounts competitors can actually log in with."""
  created_teams = []
  for i in range(num_teams):
    username = f"{username_prefix}{i + 1}"
    user, created = User.objects.get_or_create(username=username)
    if created:
      user.set_password(default_password)
      user.save()
    team, _ = Team.objects.get_or_create(
      user=user,
      competition=competition,
      defaults={"name": f"Team {i + 1}"},
    )
    created_teams.append(team)
  return created_teams


def provision_infrastructure(competition):
  """Stand-in for the real VM/network provisioning step.

  There's no Proxmox/network automation wired into the engine yet
  (see network_provisioning/), so this doesn't touch any real
  infrastructure. It just returns a placeholder status so the organizer
  flow has something to call and display until that engine exists.
  """
  return {
    "status": "not_implemented",
    "detail": (
      f"Infrastructure provisioning for '{competition.name}' is not yet implemented. "
      f"This would provision {competition.machines.count() or competition.random_machine_count or 0} "
      f"machine(s) in {competition.generation_mode} mode via Proxmox."
    ),
  }
