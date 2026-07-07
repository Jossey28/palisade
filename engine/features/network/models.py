from django.db import models

# Create your models here.
class Service(models.Model):
  name = models.CharField(max_length=100)
  host_ip = models.GenericIPAddressField()
  is_up = models.BooleanField(default=True)
  last_checked = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name
