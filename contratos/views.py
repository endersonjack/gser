from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Contrato
from .models import Contrato
from ordemservico.models import OrdemServico, Categoria
from local.models import Local
from ordemservico.models import Servico

@login_required
def selecionar_contrato(request):
    contratos = Contrato.objects.all().order_by('-data_inicio')
    total_os = OrdemServico.objects.count()  # Adiciona a contagem total de ordens
    return render(request, 'contratos/contratos.html', {
        'contratos': contratos,
        'total_os': total_os
    })

@login_required
def dashboard_geral(request):
    contratos = Contrato.objects.all()
    locais = Local.objects.all()
    categorias = Categoria.objects.all()

    # Filtros da requisição
    contrato_id = request.GET.get('contrato')
    local_id = request.GET.get('local')
    categoria_id = request.GET.get('categoria')

    # Consulta base
    ordens = OrdemServico.objects.select_related('contrato', 'local').prefetch_related('servicos')

    # Aplicação de filtros
    if contrato_id:
        ordens = ordens.filter(contrato_id=contrato_id)

    if local_id:
        ordens = ordens.filter(local_id=local_id)

    if categoria_id:
        ordens = ordens.filter(servicos__categoria_id=categoria_id).distinct()

    # Contagem por status
    status_counts = {
        "nao_iniciado": ordens.filter(situacao="nao_iniciado").count(),
        "em_andamento": ordens.filter(situacao="em_andamento").count(),
        "pendente": ordens.filter(situacao__in=["pendente", "paralisado"]).count(),
        "cancelado": ordens.filter(situacao="cancelado").count(),
        "finalizado": ordens.filter(situacao="finalizado").count(),
    }

    context = {
        'ordens_recentes': ordens.order_by('-id')[:10],
        'total_geral': ordens.count(),
        'contratos': contratos,
        'locais': locais,
        'categorias': categorias,
        'status_counts': status_counts,
        'filtros': {
            'contrato_id': contrato_id,
            'local_id': local_id,
            'categoria_id': categoria_id,
        }
    }

    return render(request, 'contratos/dashboard_geral.html', context)

@login_required
def dashboard_contrato(request, id):
    contrato = get_object_or_404(Contrato, id=id)
    request.session['contrato_id'] = id

    status_counts = {
        "nao_iniciado": OrdemServico.objects.filter(contrato=contrato, situacao="nao_iniciado").count(),
        "em_andamento": OrdemServico.objects.filter(contrato=contrato, situacao="em_andamento").count(),
        "pendente": OrdemServico.objects.filter(contrato=contrato, situacao__in=["pendente", "paralisado"]).count(),
        "cancelado": OrdemServico.objects.filter(contrato=contrato, situacao="cancelado").count(),
        "finalizado": OrdemServico.objects.filter(contrato=contrato, situacao="finalizado").count(),
    }

    # Últimos 10 serviços desse contrato
    ultimos_servicos = Servico.objects.filter(
        ordem__contrato=contrato
    ).select_related('ordem__local', 'categoria').order_by('-id')[:10]


    context = {
        'contrato': contrato,
        'status_counts': status_counts,
        'ultimos_servicos': ultimos_servicos,
    }

    return render(request, 'contratos/dashboard_contrato.html', context)
