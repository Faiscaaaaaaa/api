from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
import secrets
from .forms import CustomUserCreationForm
from .models import UserProfile


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta criada com sucesso. Pode iniciar sessão.')
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('portfolio:cursos')
        else:
            messages.error(request, 'Credenciais inválidas')
    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('portfolio:cursos')


def login_magic_link(request):
    """Recebe o email, gera token e envia o link mágico por email."""
    email = request.GET.get('email')

    if not email:
        messages.error(request, 'Introduza um email.')
        return redirect('accounts:login')

    user = User.objects.filter(email=email).first()

    if not user:
        messages.info(request, 'Se o email existir na nossa base de dados, receberá um link de acesso.')
        return redirect('accounts:login')

    # Gera token único e guarda no perfil (cria perfil se não existir)
    token = secrets.token_urlsafe(32)
    profile, _ = UserProfile.objects.get_or_create(user=user)
    profile.magic_token = token
    profile.save()

    # Constrói o link
    link = f"{settings.SITE_URL}/accounts/local/autentica/?token={token}&user_id={user.id}"

    # Envia o email
    send_mail(
        subject='Link de acesso',
        message=f'Olá {user.first_name or user.username},\n\nClique no link para entrar:\n{link}\n\nEste link é de uso único.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )

    messages.info(request, 'Se o email existir na nossa base de dados, receberá um link de acesso.')
    return render(request, 'accounts/magic_link_enviado.html')


def autentica_magic_link(request):
    """Valida o token do link mágico e autentica o utilizador."""
    token = request.GET.get('token')
    user_id = request.GET.get('user_id')

    if not token or not user_id:
        messages.error(request, 'Link inválido.')
        return redirect('accounts:login')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'Link inválido.')
        return redirect('accounts:login')

    profile, _ = UserProfile.objects.get_or_create(user=user)

    if not profile.magic_token or profile.magic_token != token:
        messages.error(request, 'Link inválido ou já utilizado.')
        return redirect('accounts:login')

    # Token válido — autentica, limpa o token
    profile.magic_token = ''
    profile.save()

    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return redirect('portfolio:landing')