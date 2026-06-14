from django.urls import path
from . import views

urlpatterns = [
    path('cursos/', views.cursos_view, name="cursos"),
    path('curso/<int:id>/', views.curso_view, name="curso"), # Nova rota com ID
    path('professores/', views.professores_view, name="professores"), # Nova rota
    path('alunos/', views.alunos_view, name="alunos"),               # Nova rota
    path('', views.cursos_view),

]