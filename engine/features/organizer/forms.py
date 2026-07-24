from django import forms
from features.competitions.models import Competition
from features.announcements.models import Announcement
from features.injects.models import Inject


class CompetitionForm(forms.ModelForm):
  class Meta:
    model = Competition
    fields = [
      "name", "start_time", "end_time",
      "difficulty", "industry",
      "generation_mode", "random_machine_count",
    ]
    widgets = {
      "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
      "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
    }


class ProvisionTeamsForm(forms.Form):
  num_teams = forms.IntegerField(min_value=1, max_value=50, initial=10)
  username_prefix = forms.CharField(max_length=20, initial="team")
  default_password = forms.CharField(max_length=50, initial="changeme")


class AnnouncementForm(forms.ModelForm):
  class Meta:
    model = Announcement
    fields = ["title"]


class InjectForm(forms.ModelForm):
  class Meta:
    model = Inject
    fields = ["title", "start_time", "due_time", "points"]
    widgets = {
      "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
      "due_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
    }
