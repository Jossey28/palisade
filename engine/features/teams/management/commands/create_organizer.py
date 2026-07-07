from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import random

class Command(BaseCommand):
  help = "Create a default organizer account"

  def handle(self, *args, **options):
    username = "default_organizer"
    password_list = ["Red", "Orange", "Yellow", "Green", "Blue", "Purple", "Brown", "Gray", "Black"]
    password = f"{random.choice(password_list)}-{random.choice(password_list)}-{random.choice(password_list)}"

    if User.objects.filter(username=username).exists():
      self.stdout.write(f"Account {username} already exists.")
      return
    
    User.objects.create_superuser(username=username, email=f"organizer+{username}@palisade.acantor.me", password=password)
    self.stdout.write(f"Created organizer account {username}:{password}")
