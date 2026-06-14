from django.contrib import admin
from django.urls import path, include
from campeonato.api import api
from campeonato import views as cam_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # API ninja (inclui /api/docs/ e /api/openapi.json por defeito)
    path('api/', api.urls),
    # consumer views
    path('pagina_colega/', cam_views.pagina_colega, name='pagina_colega'),
    path('projetos/', cam_views.projetos_list, name='projetos_list'),
    path('projetos/create/', cam_views.projetos_create, name='projetos_create'),
    path('projetos/<int:item_id>/', cam_views.projetos_detail, name='projetos_detail'),
    path('projetos/<int:item_id>/delete/', cam_views.projetos_delete, name='projetos_delete'),
]

# Servir arquivos estáticos e de media em desenvolvimento
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





