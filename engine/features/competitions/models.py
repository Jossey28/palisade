from django.db import models

# Create your models here.
class Competition(models.Model):
  name = models.CharField(max_length=100)
  start_time = models.DateTimeField()
  end_time = models.DateTimeField()
  is_active = models.BooleanField(default=False)
  scoring_interval_minutes = models.IntegerField(default=10)

  def __str__(self):
    return self.name
  
  def save(self, *args, **kwargs):
    if self.is_active:
      Competition.objects.exclude(pk=self.pk).update(is_active=False)
    super().save(*args, **kwargs)
