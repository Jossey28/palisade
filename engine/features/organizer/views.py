from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404

from features.competitions.models import Competition, MachineTemplate, CompetitionMachine
from features.injects.models import Inject, InjectSubmission

from . import provisioning, scoring
from .forms import CompetitionForm, ProvisionTeamsForm, AnnouncementForm, InjectForm


@staff_member_required
def competition_list(request):
  competitions = Competition.objects.order_by("-start_time")
  return render(request, "organizer/competition_list.html", {"competitions": competitions})


@staff_member_required
def competition_create(request):
  machine_templates = MachineTemplate.objects.all()

  if request.method == "POST":
    form = CompetitionForm(request.POST)
    if form.is_valid():
      competition = form.save()

      if competition.generation_mode == "precise":
        for template in machine_templates:
          quantity = int(request.POST.get(f"machine_{template.id}") or 0)
          if quantity > 0:
            CompetitionMachine.objects.create(
              competition=competition,
              machine_template=template,
              quantity=quantity,
            )

      messages.success(request, f"Created competition '{competition.name}'.")
      return redirect("organizer:competition_detail", pk=competition.pk)
  else:
    form = CompetitionForm()

  return render(request, "organizer/competition_form.html", {
    "form": form,
    "machine_templates": machine_templates,
  })


@staff_member_required
def competition_detail(request, pk):
  competition = get_object_or_404(Competition, pk=pk)
  return render(request, "organizer/competition_detail.html", {
    "competition": competition,
    "provision_form": ProvisionTeamsForm(),
  })


@staff_member_required
def competition_provision_teams(request, pk):
  competition = get_object_or_404(Competition, pk=pk)
  if request.method == "POST":
    form = ProvisionTeamsForm(request.POST)
    if form.is_valid():
      teams = provisioning.provision_teams(
        competition,
        form.cleaned_data["num_teams"],
        form.cleaned_data["username_prefix"],
        form.cleaned_data["default_password"],
      )
      if competition.status == "draft":
        competition.status = "provisioning"
        competition.save()
      messages.success(request, f"Provisioned {len(teams)} team(s).")
    else:
      messages.error(request, "Could not provision teams — check the form values.")
  return redirect("organizer:competition_detail", pk=competition.pk)


@staff_member_required
def competition_provision_infra(request, pk):
  competition = get_object_or_404(Competition, pk=pk)
  if request.method == "POST":
    result = provisioning.provision_infrastructure(competition)
    messages.info(request, result["detail"])
  return redirect("organizer:competition_detail", pk=competition.pk)


@staff_member_required
def competition_go_live(request, pk):
  competition = get_object_or_404(Competition, pk=pk)
  if request.method == "POST":
    competition.status = "live"
    competition.is_active = True
    competition.save()
    messages.success(request, f"{competition.name} is now live.")
  return redirect("organizer:competition_detail", pk=competition.pk)


@staff_member_required
def competition_announcements(request, pk):
  competition = get_object_or_404(Competition, pk=pk)

  if request.method == "POST":
    form = AnnouncementForm(request.POST)
    if form.is_valid():
      announcement = form.save(commit=False)
      announcement.competition = competition
      announcement.read = False
      announcement.save()
      messages.success(request, "Announcement posted.")
      return redirect("organizer:competition_announcements", pk=competition.pk)
  else:
    form = AnnouncementForm()

  announcements = competition.announcements.order_by("-published_at")
  return render(request, "organizer/announcements.html", {
    "competition": competition,
    "announcements": announcements,
    "form": form,
  })


@staff_member_required
def competition_injects(request, pk):
  competition = get_object_or_404(Competition, pk=pk)

  if request.method == "POST":
    form = InjectForm(request.POST)
    if form.is_valid():
      inject = form.save(commit=False)
      inject.competition = competition
      inject.save()
      messages.success(request, "Inject created.")
      return redirect("organizer:competition_injects", pk=competition.pk)
  else:
    form = InjectForm()

  teams = list(competition.teams.order_by("name"))
  injects = list(competition.injects.order_by("start_time"))

  submitted_pairs = set(
    InjectSubmission.objects.filter(
      inject__in=injects, team__in=teams, submitted_at__isnull=False,
    ).values_list("inject_id", "team_id")
  )

  rows = []
  for inject in injects:
    rows.append({
      "inject": inject,
      "cells": [(inject.id, team.id) in submitted_pairs for team in teams],
    })

  return render(request, "organizer/injects.html", {
    "competition": competition,
    "form": form,
    "teams": teams,
    "rows": rows,
  })


@staff_member_required
def competition_scoreboard(request, pk):
  competition = get_object_or_404(Competition, pk=pk)
  rows = scoring.compute_scoreboard(competition)
  return render(request, "organizer/scoreboard.html", {
    "competition": competition,
    "rows": rows,
  })
