from django.urls import path
from . import views

app_name = "organizer"

urlpatterns = [
  path("", views.competition_list, name="competition_list"),
  path("new/", views.competition_create, name="competition_create"),
  path("<int:pk>/", views.competition_detail, name="competition_detail"),
  path("<int:pk>/provision-teams/", views.competition_provision_teams, name="competition_provision_teams"),
  path("<int:pk>/provision-infra/", views.competition_provision_infra, name="competition_provision_infra"),
  path("<int:pk>/go-live/", views.competition_go_live, name="competition_go_live"),
  path("<int:pk>/announcements/", views.competition_announcements, name="competition_announcements"),
  path("<int:pk>/injects/", views.competition_injects, name="competition_injects"),
  path("<int:pk>/scoreboard/", views.competition_scoreboard, name="competition_scoreboard"),
]
