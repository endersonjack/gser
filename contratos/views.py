from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Contrato
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def selecionar_contrato(request):
    contratos = Contrato.objects.all().order_by('-data_inicio')
    return render(request, 'contratos/contratos.html', {'contratos': contratos})

def dashboard_contrato(request,id):
    contrato = get_object_or_404(Contrato, id=id)
    return render(request, 'contratos/dashboard_contrato.html', {'contrato': contrato})