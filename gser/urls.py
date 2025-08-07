from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.static import serve
from django.urls import re_path
from django.conf import settings
from django.conf.urls.static import static
from contratos.views import *
from local.views import *
from ordemservico.views import *



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', selecionar_contrato, name='contratos'),
    path('contrato/<int:id>/dashboard/', dashboard_contrato, name='dashboard_contrato'),
    path('dashboard-geral/', dashboard_geral, name='dashboard_geral'),
    path('locais/', listar_locais, name='locais'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('locais/editar/<int:local_id>/', editar_local, name='editar_local'),
    path('locais/excluir/<int:local_id>/', excluir_local, name='excluir_local'),
    path('locais/inserir/', inserir_local, name='inserir_local'),
    path('categorias/', listar_categorias, name='listar_categorias'),
    path('categorias/nova/', criar_categoria, name='criar_categoria'),
    path('categorias/<int:categoria_id>/editar/', editar_categoria, name='editar_categoria'),
    path('categorias/<int:categoria_id>/excluir/', excluir_categoria, name='excluir_categoria'),
    path('ordem/nova/', criar_ordem_servico, name='criar_ordem_servico'),
    path('ordem/<int:ordem_id>/', ver_ordem_servico, name='ver_ordem_servico'),
    path('ordem/<int:pk>/editar', editar_ordem_servico, name='editar_ordem_servico'),
    path('ordem/<int:ordem_id>/excluir/', excluir_ordem_servico, name='excluir_ordem_servico'),
    path('ordem/<int:ordem_id>/servicos/', adicionar_servicos_ordem, name='adicionar_servicos_ordem'),
    path('ordem/<int:ordem_id>/servico/<int:servico_id>/editar/', editar_servico, name='editar_servico'),
    path('ordem/<int:ordem_id>/servico/<int:servico_id>/', visualizar_servico, name='visualizar_servico'),
    path('ordem/<int:ordem_id>/servico/<int:servico_id>/excluir/', excluir_servico, name='excluir_servico'),

 
    path('ordem/<int:ordem_id>/servico/<int:servico_id>/fotos/', listar_albuns, name='listar_albuns'),
    path('ordem/<int:ordem_id>/servico/<int:servico_id>/fotos/novo/', criar_album, name='criar_album'),
    path('ordem/<int:ordem_id>/servico/<int:servico_id>/fotos/album/<int:album_id>/', gerenciar_album, name='gerenciar_album'),
    path('foto/<int:foto_id>/excluir/', excluir_foto, name='excluir_foto'),
    path('album/<int:album_id>/excluir/', excluir_album, name='excluir_album'),

    path('buscar/', buscar, name='buscar_os'),
    path('buscar/exportar-pdf/', exportar_resultado_pdf, name='exportar_resultado_pdf'),
    path('contrato/<int:id>/mapa-ordens/', mapa_ordens_contrato, name='mapa_ordens_contrato'),
    path('mapa-geral/', mapa_ordens_geral, name='mapa_ordens_geral'),

    path('api/mapa-ordens-geral/', api_mapa_ordens_geral, name='api_mapa_ordens_geral'),
    path('ordem/<int:ordem_id>/imprimir/', imprimir_ordem_servico, name='imprimir_ordem_servico'),




]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# No Railway, mesmo com DEBUG=False, 
# você precisa que o Whitenoise ou o gunicorn consiga servir os arquivos estáticos e de mídia manualmente.
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
