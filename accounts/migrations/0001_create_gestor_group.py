from django.db import migrations


def create_gestor_group(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    User = apps.get_model('auth', 'User')

    group, created = Group.objects.get_or_create(name='gestor-portfolio')

    # Find all content types for the portfolio app
    cts = ContentType.objects.filter(app_label='portfolio')
    perm_codenames = []
    for ct in cts:
        model = ct.model
        perm_codenames.extend([
            f'add_{model}', f'change_{model}', f'delete_{model}', f'view_{model}'
        ])

    perms = Permission.objects.filter(content_type__in=cts, codename__in=perm_codenames)
    group.permissions.set(perms)

    # Create an initial gestor user (development only) if not exists
    if not User.objects.filter(username='gestor').exists():
        gestor = User.objects.create(username='gestor', email='gestor@example.com', is_staff=True)
        gestor.set_password('gestor123')
        gestor.save()
        group.user_set.add(gestor)


def remove_gestor_group(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    User = apps.get_model('auth', 'User')
    try:
        group = Group.objects.get(name='gestor-portfolio')
        group.delete()
    except Group.DoesNotExist:
        pass
    try:
        user = User.objects.get(username='gestor')
        user.delete()
    except User.DoesNotExist:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0005_tipotecnologia_alter_makingof_descricao_processo_and_more'),
    ]

    operations = [
        migrations.RunPython(create_gestor_group, remove_gestor_group),
    ]
