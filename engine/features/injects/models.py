from django.db import models
from features.teams.models import Team

# Create your models here.
class Inject(models.Model):
  title = models.CharField(max_length=200)
  start_time = models.DateTimeField()
  due_time = models.DateTimeField()
  points = models.IntegerField()

  def __str__(self):
    return self.title

class InjectSubmission(models.Model):
  inject = models.ForeignKey(Inject, on_delete=models.CASCADE)
  team = models.ForeignKey(Team, on_delete=models.CASCADE)
  submitted_at = models.DateTimeField(null=True, blank=True)
