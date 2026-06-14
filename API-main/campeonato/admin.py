from django.contrib import admin
from .models import Equipa, Jogador, Jogo, APIKey


# --- Inline: Jogadores dentro da Equipa ---
class JogadorInline(admin.TabularInline):
    model = Jogador
    extra = 1
    fields = ('nome', 'posicao', 'idade', 'nacionalidade', 'lesionado', 'imagem')
    show_change_link = True


# --- Inline: Jogos em Casa dentro da Equipa ---
class JogoInline(admin.TabularInline):
    model = Jogo
    fk_name = 'equipa_casa'
    extra = 0
    fields = ('equipa_fora', 'data', 'golos_casa', 'golos_fora')
    readonly_fields = ('equipa_fora',)
    verbose_name = 'Jogo em casa'
    verbose_name_plural = 'Jogos em casa'


# --- Admin: Equipa ---
@admin.register(Equipa)
class EquipaAdmin(admin.ModelAdmin):
    list_display  = ('nome', 'cidade', 'AnoFundacao', 'total_jogadores')
    search_fields = ('nome', 'cidade')
    list_filter   = ('cidade',)
    inlines       = [JogadorInline, JogoInline]

    @admin.display(description='Jogadores')
    def total_jogadores(self, obj):
        return obj.jogadores.count()


# --- Admin: Jogador ---
@admin.register(Jogador)
class JogadorAdmin(admin.ModelAdmin):
    list_display  = ('nome', 'equipa', 'posicao', 'idade', 'nacionalidade', 'lesionado')
    list_filter   = ('posicao', 'nacionalidade', 'lesionado')
    search_fields = ('nome', 'equipa__nome')
    list_editable = ('lesionado',)
    list_select_related = ('equipa',)
    fieldsets = (
        (None, {
            'fields': ('equipa', 'nome', 'imagem')
        }),
        ('Detalhes', {
            'fields': ('posicao', 'idade', 'nacionalidade', 'lesionado')
        }),
    )


# --- Admin: Jogo ---
@admin.register(Jogo)
class JogoAdmin(admin.ModelAdmin):
    list_display  = ('__str__', 'data', 'resultado')
    list_filter   = ('data', 'equipa_casa')
    search_fields = ('equipa_casa__nome', 'equipa_fora__nome')
    date_hierarchy = 'data'
    list_select_related = ('equipa_casa', 'equipa_fora')

    @admin.display(description='Resultado')
    def resultado(self, obj):
        if obj.golos_casa > obj.golos_fora:
            return f'✓ Vitória {obj.equipa_casa}'
        elif obj.golos_fora > obj.golos_casa:
            return f'✓ Vitória {obj.equipa_fora}'
        return 'Empate'



class APIKeyAdmin(admin.ModelAdmin):
    list_display = ['name', 'key', 'is_active', 'expiration_date', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'key']


admin.site.register(APIKey, APIKeyAdmin)