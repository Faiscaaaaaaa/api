from django.contrib import admin
from .models import Artigo, Like, Comentario, Rating


@admin.register(Artigo)
class ArtigoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'data_criacao', 'total_likes', 'total_comentarios')
    list_filter = ('data_criacao', 'autor')
    search_fields = ('titulo', 'texto', 'autor__username')
    readonly_fields = ('data_criacao', 'data_atualizacao')
    fieldsets = (
        ('Informações do Artigo', {
            'fields': ('titulo', 'texto', 'fotografia', 'link_externo')
        }),
        ('Autor e Data', {
            'fields': ('autor', 'data_criacao', 'data_atualizacao')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('autor',)
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not change:  # Creating a new object
            obj.autor = request.user
        super().save_model(request, obj, form, change)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'artigo', 'data')
    list_filter = ('data', 'usuario')
    search_fields = ('artigo__titulo', 'usuario__username')


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('autor', 'autor_nome', 'artigo', 'data_criacao')
    list_filter = ('data_criacao', 'autor')
    search_fields = ('artigo__titulo', 'autor__username', 'autor_nome', 'texto')
    readonly_fields = ('data_criacao',)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('valor', 'artigo', 'usuario', 'data_criacao')
    list_filter = ('valor', 'data_criacao')
    search_fields = ('artigo__titulo', 'usuario__username')
    readonly_fields = ('data_criacao',)
