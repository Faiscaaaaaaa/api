from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'portfolio'

urlpatterns = [
    # Página de chegada / landing page
    path('', views.landing_view, name='landing'),

    # Páginas de Listagem Principais
    path('cursos/', views.cursos_view, name='cursos'),
    path('pessoal/', views.pessoal_view, name='pessoal'),
    path('makingof/', views.makingof_view, name='makingof'),
    path('videotutoriais/', views.videotutoriais_view, name='videotutoriais'),
    path('tfcs/', views.tfcs_view, name='tfcs'),
    path('sobre/', views.sobre_view, name='sobre'),

    # CRUD Projeto
    path('projeto/novo/', views.novo_projeto, name='novo_projeto'),
    path('projeto/editar/<int:id>/', views.edita_projeto, name='edita_projeto'),
    path('projeto/apagar/<int:id>/', views.apaga_projeto, name='apaga_projeto'),

    # CRUD Tecnologia
    path('tecnologia/nova/', views.nova_tecnologia, name='nova_tecnologia'),
    path('tecnologia/editar/<int:id>/', views.edita_tecnologia, name='edita_tecnologia'),
    path('tecnologia/apagar/<int:id>/', views.apaga_tecnologia, name='apaga_tecnologia'),

    # CRUD Competência
    path('competencia/nova/', views.nova_competencia, name='nova_competencia'),
    path('competencia/editar/<int:id>/', views.edita_competencia, name='edita_competencia'),
    path('competencia/apagar/<int:id>/', views.apaga_competencia, name='apaga_competencia'),

    # CRUD Formação
    path('formacao/nova/', views.nova_formacao, name='nova_formacao'),
    path('formacao/editar/<int:id>/', views.edita_formacao, name='edita_formacao'),
    path('formacao/apagar/<int:id>/', views.apaga_formacao, name='apaga_formacao'),

    # CRUD Unidade Curricular
    path('uc/nova/', views.nova_uc, name='nova_uc'),
    path('uc/editar/<int:id>/', views.edita_uc, name='edita_uc'),
    path('uc/apagar/<int:id>/', views.apaga_uc, name='apaga_uc'),

    # CRUD Licenciatura
    path('licenciatura/nova/', views.nova_licenciatura, name='nova_licenciatura'),
    path('licenciatura/editar/<int:id>/', views.edita_licenciatura, name='edita_licenciatura'),
    path('licenciatura/apagar/<int:id>/', views.apaga_licenciatura, name='apaga_licenciatura'),
]

# Configuração para servir ficheiros MEDIA em ambiente de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)