from django.contrib import admin
from .models import Team, Inject, InjectSubmission

# Register your models here.
class InjectSubmissionInline(admin.TabularInline):
  model = InjectSubmission
  extra = 0
  readonly_fields = ("team", "submitted_at")
  can_delete = False

@admin.register(Inject)
class InjectAdmin(admin.ModelAdmin):
  list_display = ("title", "start_time", "due_time", "points")
  inlines = [InjectSubmissionInline]

@admin.register(InjectSubmission)
class InjectSubmissionAdmin(admin.ModelAdmin):
  list_display = ("inject", "team", "submitted_at")
  list_filter = ("inject", "team")
