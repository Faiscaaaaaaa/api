from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        # Create group, permissions and a default manager user after migrations
        from django.db.models.signals import post_migrate
        from django.dispatch import receiver
        @receiver(post_migrate)
        def setup_gestor_group(sender, **kwargs):
            try:
                from django.contrib.auth.models import Group, Permission
                from django.contrib.auth import get_user_model
                from django.contrib.contenttypes.models import ContentType
                from django.apps import apps
                User = get_user_model()

                group, created = Group.objects.get_or_create(name='gestor-portfolio')

                # Collect permissions for all models in the 'portfolio' app
                perms = []
                try:
                    portfolio_app = apps.get_app_config('portfolio')
                    for model in portfolio_app.get_models():
                        ct = ContentType.objects.get_for_model(model)
                        for prefix in ('add_', 'change_', 'delete_', 'view_'):
                            codename = f"{prefix}{model._meta.model_name}"
                            try:
                                perm = Permission.objects.get(codename=codename, content_type=ct)
                                perms.append(perm)
                            except Permission.DoesNotExist:
                                pass
                except LookupError:
                    # portfolio app not ready yet
                    pass

                if perms:
                    group.permissions.set(perms)

                # Create a default manager user if not exists (development convenience)
                username = 'gestor'
                default_password = 'gestorpass'
                if not User.objects.filter(username=username).exists():
                    u = User.objects.create_user(username=username, email='gestor@example.com', password=default_password)
                    u.is_staff = True
                    u.save()
                    group.user_set.add(u)
            except Exception:
                # avoid breaking migrations if something goes wrong
                pass
