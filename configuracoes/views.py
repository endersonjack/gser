from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Empresa 

@login_required
def index(request):
    empresa = Empresa.objects.first()
    return render(request, 'configuracoes/configuracoes.html', {"empresa": empresa})

