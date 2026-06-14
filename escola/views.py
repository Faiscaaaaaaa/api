from django.shortcuts import render, get_object_or_404
from .models import Curso ,Professor, Aluno

# View para a lista de todos os cursos
def cursos_view(request):
    cursos = Curso.objects.select_related('professor').prefetch_related('alunos').all()
    return render(request, 'escola/cursos.html', {'cursos': cursos})

# Nova View para os detalhes de UM curso específico
def curso_view(request, id):
    # O get_object_or_404 é melhor que o .get() porque se o ID não existir
    # ele mostra uma página de erro limpa em vez de crashar o servidor
    curso = get_object_or_404(Curso, id=id)
    return render(request, 'escola/curso.html', {'curso': curso})

def professores_view(request):
    # Eficiente: traz os professores e já "prepara" os cursos que cada um leciona
    professores = Professor.objects.prefetch_related('cursos').all()
    return render(request, 'escola/professores.html', {'professores': professores})

def alunos_view(request):
    # Eficiente: traz os alunos e já "prepara" os cursos que cada um frequenta
    alunos = Aluno.objects.prefetch_related('cursos').all()
    return render(request, 'escola/alunos.html', {'alunos': alunos})