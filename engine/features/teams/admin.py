from django.contrib import admin
from .models import Team

# Register your models here.
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
  list_display = ("name", "user", "competition")
  list_filter = ("competition",)
  search_fields = ("name", "user__username")
