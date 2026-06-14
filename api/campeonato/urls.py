from django.urls import include, path
from .api import api as campeonato_api
from . import views as cam_views

urlpatterns = [
    # Redirect root api to docs
    path('', cam_views.api_redirect_to_docs, name='api-root-redirect'),

    # Consumer views for HTML templates
    path('pagina_colega/', cam_views.pagina_colega, name='pagina_colega'),
    path('projetos/', cam_views.projetos_list, name='projetos_list'),
    path('projetos/create/', cam_views.projetos_create, name='projetos_create'),
    path('projetos/<int:item_id>/', cam_views.projetos_detail, name='projetos_detail'),
    path('projetos/<int:item_id>/delete/', cam_views.projetos_delete, name='projetos_delete'),

    # API Ninja routes
    path('', include((campeonato_api.urls[0], campeonato_api.urls[1]), namespace=campeonato_api.urls[2])),
]
