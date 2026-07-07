from django.contrib import admin
from .models import Team, Inject, InjectSubmission

admin.site.register(Team)
admin.site.register(Inject)
admin.site.register(InjectSubmission)

# Register your models here.
