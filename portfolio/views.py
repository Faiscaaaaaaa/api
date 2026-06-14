from django.shortcuts import render, redirect, get_object_or_404
from .models import Licenciatura, Competencia, Formacao, InteressePessoal, MakingOf, TFC, Projeto, Tecnologia, TipoTecnologia, UnidadeCurricular
from .forms import ProjetoForm, TecnologiaForm, CompetenciaForm, FormacaoForm, UnidadeCurricularForm, LicenciaturaForm

# --- VISTAS DE LISTAGEM (Páginas Principais) ---

def landing_view(request):
    return render(request, 'portfolio/landing.html')

def cursos_view(request):
    licenciaturas = Licenciatura.objects.prefetch_related('ucs__projeto_set__tecnologias').all()
    return render(request, 'portfolio/cursos.html', {'licenciaturas': licenciaturas, 'is_gestor': _is_gestor(request.user)})

def pessoal_view(request):
    context = {
        'competencias': Competencia.objects.prefetch_related('tecnologias_associadas', 'projetos_associados').all(),
        'formacoes': Formacao.objects.all(),
        'interesses': InteressePessoal.objects.all(),
        'tecnologias': Tecnologia.objects.all(),
        'is_gestor': _is_gestor(request.user),
        'linkedin_url': 'https://www.linkedin.com/in/diogo-fa%C3%ADsca-ab22ab263/',
        'discord_url': 'https://discord.gg/fallinngg',
        'github_repo': 'https://github.com/Diogo-Faisca-a22408949/DjangoPortfolio',
    }
    return render(request, 'portfolio/pessoal.html', context)

def makingof_view(request):
    makingofs = MakingOf.objects.all().order_by('-data')
    return render(request, 'portfolio/makingof.html', {'makingofs': makingofs})

def tfcs_view(request):
    tfcs = TFC.objects.all().order_by('-ano')
    return render(request, 'portfolio/tfcs.html', {'tfcs': tfcs})

def sobre_view(request):
    # O prefetch_related carrega logo as tecnologias associadas a cada tipo
    tipos_tecnologia = TipoTecnologia.objects.prefetch_related('tecnologias').all()
    return render(request, 'portfolio/sobre.html', {
        'tipos': tipos_tecnologia,
        'github_repo': 'https://github.com/Diogo-Faisca-a22408949/DjangoPortfolio'
    })

def videotutoriais_view(request):
    return render(request, 'portfolio/videotutoriais.html')

# --- LÓGICA GENÉRICA PARA CRUD (Auxiliares) ---

def criar_item(request, form_class, redirect_url, template_title):
    form = form_class(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect(f'portfolio:{redirect_url}')
    return render(request, 'portfolio/form_template.html', {'form': form, 'titulo': template_title})

def editar_item(request, id, model_class, form_class, redirect_url, template_title):
    item = get_object_or_404(model_class, id=id)
    form = form_class(request.POST or None, request.FILES or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect(f'portfolio:{redirect_url}')
    return render(request, 'portfolio/form_template.html', {'form': form, 'titulo': template_title})

def apagar_item(request, id, model_class, redirect_url):
    item = get_object_or_404(model_class, id=id)
    if request.method == 'POST':
        item.delete()
        return redirect(f'portfolio:{redirect_url}')
    return render(request, 'portfolio/confirm_delete.html', {'item': item})

# --- MAPEAMENTO DAS FUNÇÕES CRUD ---

# Projetos
def novo_projeto(request): return criar_item(request, ProjetoForm, 'cursos', 'Novo Projeto')
def edita_projeto(request, id): return editar_item(request, id, Projeto, ProjetoForm, 'cursos', 'Editar Projeto')
def apaga_projeto(request, id): return apagar_item(request, id, Projeto, 'cursos')

# Tecnologias
def nova_tecnologia(request): return criar_item(request, TecnologiaForm, 'pessoal', 'Nova Tecnologia')
def edita_tecnologia(request, id): return editar_item(request, id, Tecnologia, TecnologiaForm, 'pessoal', 'Editar Tecnologia')
def apaga_tecnologia(request, id): return apagar_item(request, id, Tecnologia, 'pessoal')

# Competências
def nova_competencia(request): return criar_item(request, CompetenciaForm, 'pessoal', 'Nova Competência')
def edita_competencia(request, id): return editar_item(request, id, Competencia, CompetenciaForm, 'pessoal', 'Editar Competência')
def apaga_competencia(request, id): return apagar_item(request, id, Competencia, 'pessoal')

# Formações
def nova_formacao(request): return criar_item(request, FormacaoForm, 'pessoal', 'Nova Formação')
def edita_formacao(request, id): return editar_item(request, id, Formacao, FormacaoForm, 'pessoal', 'Editar Formação')
def apaga_formacao(request, id): return apagar_item(request, id, Formacao, 'pessoal')

# SECURITY: decorated wrappers that restrict CRUD to authenticated gestores
from django.contrib.auth.decorators import login_required, user_passes_test

def _is_gestor(user):
    return user.is_authenticated and user.groups.filter(name='gestor-portfolio').exists()

# Decorated CRUD wrappers (override the simple functions above)
@login_required
@user_passes_test(_is_gestor)
def novo_projeto(request):
    return criar_item(request, ProjetoForm, 'cursos', 'Novo Projeto')

@login_required
@user_passes_test(_is_gestor)
def edita_projeto(request, id):
    return editar_item(request, id, Projeto, ProjetoForm, 'cursos', 'Editar Projeto')

@login_required
@user_passes_test(_is_gestor)
def apaga_projeto(request, id):
    return apagar_item(request, id, Projeto, 'cursos')

@login_required
@user_passes_test(_is_gestor)
def nova_tecnologia(request):
    return criar_item(request, TecnologiaForm, 'pessoal', 'Nova Tecnologia')

@login_required
@user_passes_test(_is_gestor)
def edita_tecnologia(request, id):
    return editar_item(request, id, Tecnologia, TecnologiaForm, 'pessoal', 'Editar Tecnologia')

@login_required
@user_passes_test(_is_gestor)
def apaga_tecnologia(request, id):
    return apagar_item(request, id, Tecnologia, 'pessoal')

@login_required
@user_passes_test(_is_gestor)
def nova_competencia(request):
    return criar_item(request, CompetenciaForm, 'pessoal', 'Nova Competência')

@login_required
@user_passes_test(_is_gestor)
def edita_competencia(request, id):
    return editar_item(request, id, Competencia, CompetenciaForm, 'pessoal', 'Editar Competência')

@login_required
@user_passes_test(_is_gestor)
def apaga_competencia(request, id):
    return apagar_item(request, id, Competencia, 'pessoal')

@login_required
@user_passes_test(_is_gestor)
def nova_formacao(request):
    return criar_item(request, FormacaoForm, 'pessoal', 'Nova Formação')

@login_required
@user_passes_test(_is_gestor)
def edita_formacao(request, id):
    return editar_item(request, id, Formacao, FormacaoForm, 'pessoal', 'Editar Formação')

@login_required
@user_passes_test(_is_gestor)
def apaga_formacao(request, id):
    return apagar_item(request, id, Formacao, 'pessoal')

# Unidades Curriculares
@login_required
@user_passes_test(_is_gestor)
def nova_uc(request):
    return criar_item(request, UnidadeCurricularForm, 'cursos', 'Nova Unidade Curricular')

@login_required
@user_passes_test(_is_gestor)
def edita_uc(request, id):
    return editar_item(request, id, UnidadeCurricular, UnidadeCurricularForm, 'cursos', 'Editar Unidade Curricular')

@login_required
@user_passes_test(_is_gestor)
def apaga_uc(request, id):
    return apagar_item(request, id, UnidadeCurricular, 'cursos')

# Licenciaturas
@login_required
@user_passes_test(_is_gestor)
def nova_licenciatura(request):
    return criar_item(request, LicenciaturaForm, 'cursos', 'Nova Licenciatura')

@login_required
@user_passes_test(_is_gestor)
def edita_licenciatura(request, id):
    return editar_item(request, id, Licenciatura, LicenciaturaForm, 'cursos', 'Editar Licenciatura')

@login_required
@user_passes_test(_is_gestor)
def apaga_licenciatura(request, id):
    return apagar_item(request, id, Licenciatura, 'cursos')
