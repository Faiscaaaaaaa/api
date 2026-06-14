from django.contrib import admin
from .models import *

@admin.register(TFC)
class TFCAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'licenciatura', 'ano', 'destaque') 
    search_fields = ('titulo', 'autores')
    list_filter = ('licenciatura', 'ano', 'destaque')

admin.site.register(Licenciatura)
admin.site.register(Tecnologia)
admin.site.register(UnidadeCurricular)
admin.site.register(Projeto)
admin.site.register(Competencia)
admin.site.register(Formacao)
admin.site.register(MakingOf)
admin.site.register(InteressePessoal)