from django.db import migrations

MACHINE_TEMPLATES = [
    ("Windows Server 2019 - Domain Controller", "windows", "Domain Controller"),
    ("Windows Server 2019 - IIS Web Server", "windows", "Web Server"),
    ("Windows 10 Workstation", "windows", "Workstation"),
    ("Ubuntu 22.04 - Web Server", "linux", "Web Server"),
    ("Ubuntu 22.04 - Mail Server", "linux", "Mail Server"),
    ("Rocky Linux 9 - Database Server", "linux", "Database Server"),
    ("pfSense Firewall", "network", "Firewall"),
    ("Kali Linux - Jump Box", "linux", "Jump Box"),
]


def seed_machine_templates(apps, schema_editor):
    MachineTemplate = apps.get_model("competitions", "MachineTemplate")
    for name, os_family, role in MACHINE_TEMPLATES:
        MachineTemplate.objects.get_or_create(name=name, defaults={"os_family": os_family, "role": role})


def unseed_machine_templates(apps, schema_editor):
    MachineTemplate = apps.get_model("competitions", "MachineTemplate")
    MachineTemplate.objects.filter(name__in=[name for name, _, _ in MACHINE_TEMPLATES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '0002_machinetemplate_competition_difficulty_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_machine_templates, unseed_machine_templates),
    ]
