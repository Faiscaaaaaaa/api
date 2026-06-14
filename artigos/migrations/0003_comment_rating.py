from django.db import migrations, models
from django.core.validators import MinValueValidator, MaxValueValidator


def create_sample_artigos(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Artigo = apps.get_model('artigos', 'Artigo')

    gestor, created = User.objects.get_or_create(
        username='gestor',
        defaults={
            'email': 'gestor@example.com',
        }
    )
    if created:
        gestor.set_password('gestorpass')
        gestor.save()

    sample_artigos = [
        {
            'titulo': 'Design Responsivo e Acessível',
            'texto': 'Neste artigo exploro como criar interfaces que se adaptam a diferentes tamanhos de ecrã, garantindo também uma experiência acessível para todos os utilizadores.',
            'link_externo': 'https://developer.mozilla.org/pt-BR/docs/Learn/CSS/CSS_layout/Responsive_Design',
        },
        {
            'titulo': 'Django: Modelando Conteúdo Dinâmico',
            'texto': 'Vamos analisar a modelação de dados no Django, incluindo relações entre modelos e boas práticas para criar aplicações web escaláveis.',
            'link_externo': 'https://docs.djangoproject.com/pt-br/4.2/topics/db/models/',
        },
        {
            'titulo': 'Workflow Git e Controle de Versão',
            'texto': 'Uma boa rotina de commits, branches e pull requests torna o desenvolvimento mais seguro e colaborativo. Este artigo descreve um fluxo de trabalho eficiente para projetos web.',
            'link_externo': 'https://www.atlassian.com/br/git/tutorials/comparing-workflows',
        },
    ]

    for item in sample_artigos:
        Artigo.objects.get_or_create(
            titulo=item['titulo'],
            defaults={
                'texto': item['texto'],
                'link_externo': item['link_externo'],
                'autor': gestor,
            }
        )


class Migration(migrations.Migration):

    dependencies = [
        ('artigos', '0002_create_autores_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='autor',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.CASCADE, to='auth.user'),
        ),
        migrations.AddField(
            model_name='comentario',
            name='autor_nome',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('artigo', models.ForeignKey(on_delete=models.CASCADE, related_name='ratings', to='artigos.artigo')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=models.CASCADE, to='auth.user')),
            ],
            options={
                'ordering': ['-data_criacao'],
                'verbose_name_plural': 'Avaliações',
            },
        ),
        migrations.RunPython(create_sample_artigos),
    ]
