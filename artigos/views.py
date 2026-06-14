from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Avg
from .models import Artigo, Like, Comentario, Rating
from .forms import ArtigoForm, ComentarioForm, RatingForm


def _is_blogger(user):
    """Verificar se o utilizador é membro do grupo 'bloggers'"""
    return user.is_authenticated and user.groups.filter(name='bloggers').exists()


# --- VISTAS DE LISTAGEM ---

def lista_artigos(request):
    """Listagem pública de todos os artigos"""
    artigos = Artigo.objects.all().order_by('-data_criacao')
    return render(request, 'artigos/lista_artigos.html', {
        'artigos': artigos,
        'is_blogger': _is_blogger(request.user),
    })


def detalhe_artigo(request, id):
    """Detalhe de um artigo com comentários, rating e likes"""
    artigo = get_object_or_404(Artigo, id=id)
    comentarios = artigo.comentarios.all()
    usuario_gostou = False
    
    if request.user.is_authenticated:
        usuario_gostou = artigo.likes.filter(usuario=request.user).exists()
    
    form_comentario = ComentarioForm()
    form_rating = RatingForm()
    
    context = {
        'artigo': artigo,
        'comentarios': comentarios,
        'usuario_gostou': usuario_gostou,
        'form_comentario': form_comentario,
        'form_rating': form_rating,
        'is_blogger': _is_blogger(request.user),
        'pode_editar': request.user == artigo.autor,
    }
    return render(request, 'artigos/detalhe_artigo.html', context)


# --- CRUD DE ARTIGOS ---

@login_required
@user_passes_test(_is_blogger)
def criar_artigo(request):
    """Criar novo artigo (apenas para bloggers)"""
    if request.method == 'POST':
        form = ArtigoForm(request.POST, request.FILES)
        if form.is_valid():
            artigo = form.save(commit=False)
            artigo.autor = request.user
            artigo.save()
            messages.success(request, 'Artigo criado com sucesso!')
            return redirect('artigos:detalhe_artigo', id=artigo.id)
    else:
        form = ArtigoForm()
    
    return render(request, 'artigos/form_artigo.html', {
        'form': form,
        'titulo': 'Novo Artigo'
    })


@login_required
@user_passes_test(_is_blogger)
def editar_artigo(request, id):
    """Editar artigo (apenas para o autor)"""
    artigo = get_object_or_404(Artigo, id=id)
    
    # Verificar se o utilizador é o autor
    if request.user != artigo.autor:
        messages.error(request, 'Apenas o autor pode editar este artigo.')
        return redirect('artigos:detalhe_artigo', id=artigo.id)
    
    if request.method == 'POST':
        form = ArtigoForm(request.POST, request.FILES, instance=artigo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Artigo atualizado com sucesso!')
            return redirect('artigos:detalhe_artigo', id=artigo.id)
    else:
        form = ArtigoForm(instance=artigo)
    
    return render(request, 'artigos/form_artigo.html', {
        'form': form,
        'titulo': 'Editar Artigo'
    })


@login_required
@user_passes_test(_is_blogger)
def deletar_artigo(request, id):
    """Deletar artigo (apenas para o autor)"""
    artigo = get_object_or_404(Artigo, id=id)
    
    # Verificar se o utilizador é o autor
    if request.user != artigo.autor:
        messages.error(request, 'Apenas o autor pode deletar este artigo.')
        return redirect('artigos:detalhe_artigo', id=artigo.id)
    
    if request.method == 'POST':
        titulo = artigo.titulo
        artigo.delete()
        messages.success(request, f'Artigo "{titulo}" foi deletado.')
        return redirect('artigos:lista_artigos')
    
    return render(request, 'artigos/confirmar_delete.html', {
        'artigo': artigo
    })


# --- LIKES ---

@login_required
@require_POST
def toggle_like(request, id):
    """Ativar/desativar like em um artigo"""
    artigo = get_object_or_404(Artigo, id=id)
    like, created = Like.objects.get_or_create(artigo=artigo, usuario=request.user)
    
    if not created:
        like.delete()
        gostou = False
    else:
        gostou = True
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'gostou': gostou,
            'total_likes': artigo.total_likes()
        })
    return redirect('artigos:detalhe_artigo', id=artigo.id)


@require_POST
def adicionar_rating(request, id):
    """Adicionar pontuação a um artigo"""
    artigo = get_object_or_404(Artigo, id=id)
    form = RatingForm(request.POST)
    
    if form.is_valid():
        rating = form.save(commit=False)
        rating.artigo = artigo
        if request.user.is_authenticated:
            rating.usuario = request.user
        rating.save()
        messages.success(request, 'Pontuação registada com sucesso!')
    else:
        messages.error(request, 'Não foi possível registar a pontuação. Escolha um valor entre 1 e 5.')
    
    return redirect('artigos:detalhe_artigo', id=artigo.id)

@require_POST
def adicionar_comentario(request, id):
    """Adicionar comentário a um artigo"""
    artigo = get_object_or_404(Artigo, id=id)
    form = ComentarioForm(request.POST)
    
    if form.is_valid():
        comentario = form.save(commit=False)
        comentario.artigo = artigo
        if request.user.is_authenticated:
            comentario.autor = request.user
            if not comentario.autor_nome:
                comentario.autor_nome = request.user.username
        else:
            comentario.autor = None
            if not comentario.autor_nome:
                comentario.autor_nome = 'Visitante'
        comentario.save()
        messages.success(request, 'Comentário adicionado com sucesso!')
    else:
        messages.error(request, 'Não foi possível adicionar o comentário. Verifique os dados e tente novamente.')
    
    return redirect('artigos:detalhe_artigo', id=artigo.id)
