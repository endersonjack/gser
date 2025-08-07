from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Contrato
from .models import Contrato
from ordemservico.models import OrdemServico, Categoria
from local.models import Local
from ordemservico.models import Servico
from django.urls import reverse
import json
from django.db.models import Count
from django.utils.timesince import timesince



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

    # Consulta base
    ordens = OrdemServico.objects.select_related('contrato', 'local').prefetch_related('servicos')

    # Filtros da requisição
    contrato_id = request.GET.get('contrato')
    local_id = request.GET.get('local')
    categoria_id = request.GET.get('categoria')

    # Aplicação de filtros
    if contrato_id:
        ordens = ordens.filter(contrato_id=contrato_id)

    if local_id:
        ordens = ordens.filter(local_id=local_id)

    if categoria_id:
        ordens = ordens.filter(servicos__categoria_id=categoria_id).distinct()

    # Totais globais (com base nas ordens filtradas)
    total_os = ordens.count()
    total_servicos = Servico.objects.filter(ordem__in=ordens).count()
    total_finalizadas = ordens.filter(situacao="finalizado").count()
    percentual_finalizadas = round((total_finalizadas / total_os) * 100, 1) if total_os else 0
    ultima_os = ordens.order_by('-id').first()

    # Contagem por status
    status_counts = {
        "nao_iniciado": ordens.filter(situacao="nao_iniciado").count(),
        "em_andamento": ordens.filter(situacao="em_andamento").count(),
        "pendente": ordens.filter(situacao__in=["pendente", "paralisado"]).count(),
        "cancelado": ordens.filter(situacao="cancelado").count(),
        "finalizado": total_finalizadas,
    }

    context = {
        'ordens_recentes': ordens.order_by('-id')[:10],
        'total_geral': total_os,
        'contratos': contratos,
        'locais': locais,
        'categorias': categorias,
        'status_counts': status_counts,
        'total_os': total_os,
        'total_servicos': total_servicos,
        'percentual_finalizadas': percentual_finalizadas,
        'ultima_os': ultima_os,
        'filtros': {
            'contrato_id': contrato_id,
            'local_id': local_id,
            'categoria_id': categoria_id,
        }
    }

    return render(request, 'contratos/dashboard_geral.html', context)


from datetime import timedelta
from django.utils import timezone
from django.db.models import Count

@login_required
def dashboard_contrato(request, id):
    contrato = get_object_or_404(Contrato, id=id)
    request.session['contrato_id'] = id

    ordens = OrdemServico.objects.filter(contrato=contrato)

    # === ALERTAS ===
    hoje = timezone.now().date()
    ordens_30_dias = ordens.filter(situacao="nao_iniciado", data_inicio__lt=hoje - timedelta(days=30))
    ordens_sem_servicos = ordens.annotate(qtd_servicos=Count('servicos')).filter(qtd_servicos=0)

    # Calcula texto do tipo "há X dias"
    top_5_ordens_antigas = ordens.filter(situacao="nao_iniciado").order_by('data_inicio')[:5]
    for os in top_5_ordens_antigas:
        dias = (hoje - os.data_inicio).days
        os.tempo_espera = f"{dias} dia{'s' if dias != 1 else ''}"

    # === DEMAIS DADOS ===
    status_counts = {
        "nao_iniciado": ordens.filter(situacao="nao_iniciado").count(),
        "em_andamento": ordens.filter(situacao="em_andamento").count(),
        "pendente": ordens.filter(situacao__in=["pendente", "paralisado"]).count(),
        "cancelado": ordens.filter(situacao="cancelado").count(),
        "finalizado": ordens.filter(situacao="finalizado").count(),
    }

    total_os = ordens.count()
    total_servicos = Servico.objects.filter(ordem__contrato=contrato).count()
    ultimas_ordens = ordens.order_by('-id')[:10]

    percentual_finalizadas = round((status_counts['finalizado'] / total_os) * 100) if total_os else 0

    status_info = {
        "nao_iniciado": {"label": "Não Iniciado", "color": "secondary", "icon": "circle"},
        "em_andamento": {"label": "Em Andamento", "color": "primary", "icon": "spinner"},
        "pendente": {"label": "Pendente/Paralisado", "color": "warning text-dark", "icon": "pause-circle"},
        "cancelado": {"label": "Cancelado", "color": "danger", "icon": "times-circle"},
        "finalizado": {"label": "Finalizado", "color": "success", "icon": "check-circle"},
    }

    ultimos_servicos = Servico.objects.filter(ordem__contrato=contrato).select_related('ordem__local', 'categoria').order_by('-id')[:10]

    context = {
        'contrato': contrato,
        'status_counts': status_counts,
        'status_info': status_info,
        'total_os': total_os,
        'total_servicos': total_servicos,
        'ultimas_ordens': ultimas_ordens,
        'percentual_finalizadas': percentual_finalizadas,
        'ultimos_servicos': ultimos_servicos,
        # ALERTAS:
        'ordens_30_dias': ordens_30_dias,
        'ordens_sem_servicos': ordens_sem_servicos,
        'top_5_ordens_antigas': top_5_ordens_antigas,
    }

    return render(request, 'contratos/dashboard_contrato.html', context)



@login_required
def mapa_ordens_contrato(request, id):
    contrato = get_object_or_404(Contrato, id=id)

    ordens = OrdemServico.objects.filter(contrato=contrato).select_related('local')

    locais_com_coords = []
    for ordem in ordens:
        local = ordem.local
        if local and local.latitude is not None and local.longitude is not None:
            locais_com_coords.append({
                'id': ordem.id,
                'numero': getattr(ordem, 'numero_formatado', str(ordem.numero).zfill(4)),
                'local_nome': local.nome,
                'lat': float(local.latitude),
                'lng': float(local.longitude),
                'situacao': ordem.get_situacao_display(),
                'url': reverse('ver_ordem_servico', args=[ordem.id])
            })


    # for os in OrdemServico.objects.all():
    #     print(f"OS #{os.numero} → Local: {os.local} → LAT: {getattr(os.local, 'latitude', None)}")

    return render(request, 'contratos/mapa_ordens_contrato.html', {
        'contrato': contrato,
        'marcadores': json.dumps(locais_com_coords)
    })

@login_required
def mapa_ordens_geral(request):
    ordens = OrdemServico.objects.select_related('local', 'contrato')
    contratos = Contrato.objects.all()

    locais_com_coords = []
    for ordem in ordens:
        local = ordem.local
        if local and local.latitude and local.longitude:
            locais_com_coords.append({
                'id': ordem.id,
                'numero': getattr(ordem, 'numero_formatado', str(ordem.numero).zfill(4)),
                'local_nome': local.nome,
                'lat': float(local.latitude),
                'lng': float(local.longitude),
                'situacao': ordem.get_situacao_display(),
                'contrato': ordem.contrato.numero,
                'url': reverse('ver_ordem_servico', args=[ordem.id])
            })

    return render(request, 'contratos/mapa_ordens_geral.html', {
        'marcadores': json.dumps(locais_com_coords),
        'contratos': contratos,
    })


from django.http import JsonResponse

@login_required
def api_mapa_ordens_geral(request):
    ordens = OrdemServico.objects.select_related('local', 'contrato')

    locais_com_coords = []
    for ordem in ordens:
        local = ordem.local
        if local and local.latitude and local.longitude:
            locais_com_coords.append({
                'id': ordem.id,
                'numero': getattr(ordem, 'numero_formatado', str(ordem.numero).zfill(4)),
                'local_nome': local.nome,
                'lat': float(local.latitude),
                'lng': float(local.longitude),
                'situacao': ordem.get_situacao_display(),
                'contrato': ordem.contrato.numero,
                'url': reverse('ver_ordem_servico', args=[ordem.id])
            })

    return JsonResponse({'marcadores': locais_com_coords})
