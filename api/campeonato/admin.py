from django.contrib import admin

from .models import Equipa, Jogador, Jogo, APIKey


@admin.register(Equipa)
class EquipaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cidade', 'ano_fundacao')


@admin.register(Jogador)
class JogadorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'equipa', 'idade', 'posicao', 'nacionalidade', 'lesionado')


@admin.register(Jogo)
class JogoAdmin(admin.ModelAdmin):
    list_display = ('equipa_casa', 'equipa_fora', 'data', 'golos_casa', 'golos_fora')


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('name', 'key', 'is_active', 'expiration_date', 'created_at')
