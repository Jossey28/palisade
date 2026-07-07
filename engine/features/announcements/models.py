from django.db import models

# Create your models here.
class Announcement(models.Model):
  title = models.CharField(max_length=200)
  published_at = models.DateTimeField(auto_now_add=True)
  read = models.BooleanField() # this is a potential addition, it is not currently implemented

  def __str__(self):
    return self.title
