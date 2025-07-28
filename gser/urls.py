"""
URL configuration for gser project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from contratos.views import *
from local.views import listar_locais, editar_local, excluir_local, inserir_local

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', selecionar_contrato, name='contratos'),
    path('contrato/<int:id>/dashboard/', dashboard_contrato, name='dashboard_contrato'),
    path('locais/', listar_locais, name='locais'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('locais/editar/<int:local_id>/', editar_local, name='editar_local'),
    path('locais/excluir/<int:local_id>/', excluir_local, name='excluir_local'),
    path('locais/inserir/', inserir_local, name='inserir_local'),

]
