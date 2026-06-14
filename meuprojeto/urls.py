from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from artigos import views as artigos_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path("escola/", include("escola.urls")),
    path('accounts/', include('allauth.urls')),
    path('accounts/local/', include('accounts.urls')),
    path('artigos/', include('artigos.urls')),
    path('artigo_detalhe/<int:id>/', artigos_views.detalhe_artigo, name='artigo_detalhe'),
    path('', include('portfolio.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # ← adiciona esta linha