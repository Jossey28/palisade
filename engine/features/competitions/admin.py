from django.contrib import admin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import path
from django import forms
from .models import Competition
from features.teams.models import Team

# Register your models here.
class BulkCreateTeamsForm(forms.Form):
  num_teams = forms.IntegerField(min_value=1, max_value=50, initial=10)
  username_prefix = forms.CharField(max_length=20, initial="team")
  default_password = forms.CharField(max_length=50, initial="changeme")

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
  list_display = ("name", "start_time", "end_time", "is_active")
  actions = ["activate_competition"]

  def get_urls(self):
    urls = super().get_urls()
    custom = [path("<int:competition_id>/bulk-create-items/", self.bulk_create_teams, name="bulk_create_items"),]
    return custom + super().get_urls()
  
  def bulk_create_teams(self, request, pk):
    competition = Competition.objects.get(pk=pk)
    form = BulkCreateTeamsForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
      for i in range (form.cleaned_data["nums"]):
        username = f"{form.cleaned_data['username_prefix']}{i+1}"
        user, created = User.objects.get_or_create(username=username)
        if created:
          user.set_password(form.cleaned_data["default_password"])
          user.save()
        Team.objects.get_or_create(user=user, competition=competition, defaults={"name": f"Team {i+1}"})
      
      self.message_user(request, f"Created teams for {competition.name}.")
      return redirect("..")
  
    return render(request, "admin/bulk_create_teams.html", {"form": form, "competition": competition})

  def activate_competition(self, request, queryset):
    if queryset.count() != 1:
      self.message_user(request, "Select exactly one competition to activate.", level="error")
      return
    
    comp = queryset.first()
    comp.is_active = True
    comp.save()
    self.message_user(request, f"{comp.name} is now live.")
  
  activate_competition.short_description = "Set as active competition"
