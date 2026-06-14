from django.urls import path
from . import views

app_name = 'artigos'

urlpatterns = [
    # Listagem e detalhe
    path('', views.lista_artigos, name='lista_artigos'),
    path('artigo_detalhe/<int:id>/', views.detalhe_artigo, name='detalhe_artigo'),
    
    # CRUD
    path('criar/', views.criar_artigo, name='criar_artigo'),
    path('<int:id>/editar/', views.editar_artigo, name='editar_artigo'),
    path('<int:id>/deletar/', views.deletar_artigo, name='deletar_artigo'),
    
    # Likes
    path('<int:id>/like/', views.toggle_like, name='toggle_like'),
    path('<int:id>/avaliar/', views.adicionar_rating, name='adicionar_rating'),
    
    # Comentários
    path('<int:id>/comentario/', views.adicionar_comentario, name='adicionar_comentario'),
]
