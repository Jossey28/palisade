from django.contrib import admin
from .models import Competition, MachineTemplate, CompetitionMachine

# Register your models here.
@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
  list_display = ("name", "status", "difficulty", "industry", "start_time", "end_time", "is_active")
  list_filter = ("status", "difficulty", "industry")


@admin.register(MachineTemplate)
class MachineTemplateAdmin(admin.ModelAdmin):
  list_display = ("name", "os_family", "role")
  list_filter = ("os_family",)


@admin.register(CompetitionMachine)
class CompetitionMachineAdmin(admin.ModelAdmin):
  list_display = ("competition", "machine_template", "quantity")
  list_filter = ("competition",)
