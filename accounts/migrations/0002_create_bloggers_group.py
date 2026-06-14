from django.db import migrations


def create_bloggers_group(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.get_or_create(name='bloggers')


def reverse_bloggers_group(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name='bloggers').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_create_gestor_group'),
    ]

    operations = [
        migrations.RunPython(create_bloggers_group, reverse_bloggers_group),
    ]
