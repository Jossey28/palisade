from django.db import models
from django.contrib.auth.models import User
from features.competitions.models import Competition

# Create your models here.
class Team(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name="teams")
  name = models.CharField(max_length=50)

  def __str__(self):
    return f"{self.name} {self.competition.name}"
