from .models import Categoria
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CategoriaForm 
from django.contrib import messages
from .models import OrdemServico, Servico
from .forms import OrdemServicoForm, ServicoForm, OrdemServicoEditForm
from django.forms import inlineformset_factory
from .models import Album, Foto, OrdemServico, Servico
from .forms import AlbumForm, FotoForm

@login_required
def listar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'categorias/listar_categorias.html', {'categorias': categorias})

@login_required
def criar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria criada com sucesso.')
            return redirect('listar_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'categorias/criar_categoria.html', {'form': form})


@login_required
def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria atualizada com sucesso.')
            return redirect('listar_categorias')
        else:
            messages.error(request, 'Erro ao atualizar categoria.')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'categorias/editar_categoria.html', {'form': form, 'categoria': categoria})

@require_POST
@login_required
def excluir_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    categoria.delete()
    messages.success(request, 'Categoria excluída com sucesso.')
    return redirect('listar_categorias')


@login_required
def criar_ordem_servico(request):
    if request.method == 'POST':
        form = OrdemServicoForm(request.POST)
        if form.is_valid():
            ordem = form.save()
            messages.success(request, "Ordem de serviço criada com sucesso.")
            return redirect('ver_ordem_servico', ordem.id)
    else:
        form = OrdemServicoForm(initial={'situacao': 'nao_iniciado'})

    return render(request, 'ordemservico/criar_ordem_servico.html', {
        'form': form,
    })



@login_required
def ver_ordem_servico(request, ordem_id):
    ordem = get_object_or_404(OrdemServico, id=ordem_id)
    return render(request, 'ordemservico/ver_ordem_servico.html', {'ordem': ordem})


@login_required
def editar_ordem_servico(request, pk):
    ordem = get_object_or_404(OrdemServico, pk=pk)

    if request.method == 'POST':
        form = OrdemServicoEditForm(request.POST, instance=ordem)
        if form.is_valid():
            form.save()
            messages.success(request, "Ordem de Serviço atualizada com sucesso.")
            return redirect('ver_ordem_servico', ordem_id=ordem.pk)
    else:
        form = OrdemServicoEditForm(instance=ordem)
        # # desabilita o campo contrato no formulário (para exibição apenas)
        # form.fields['contrato'].disabled = True

    return render(request, 'ordemservico/editar_ordem_servico.html', {
        'form': form,
        'ordem': ordem,
    })


@login_required
def excluir_ordem_servico(request, ordem_id):
    ordem = get_object_or_404(OrdemServico, id=ordem_id)

    if request.method == "POST":
        contrato_id = ordem.contrato.id  # salva para redirecionar ao painel do contrato
        ordem.delete()
        messages.success(request, "Ordem de Serviço excluída com sucesso.")
        return redirect('dashboard_contrato', id=contrato_id)

    # Segurança: se for GET, redireciona para visualizar a ordem
    return redirect('ver_ordem_servico', ordem_id=ordem.id)


@login_required
def adicionar_servicos_ordem(request, ordem_id):
    ordem = get_object_or_404(OrdemServico, id=ordem_id)

    # inlineformset associa automaticamente cada serviço à ordem
    ServicoFormSet = inlineformset_factory(
        OrdemServico,
        Servico,
        form=ServicoForm,
        extra=1,
        can_delete=False
    )

    if request.method == 'POST':
        formset = ServicoFormSet(request.POST, instance=ordem, prefix='servicos')


        if formset.is_valid():
            formset.save()
            messages.success(request, "Serviço salvo com sucesso.")

            if 'encerrar' in request.POST:
                return redirect('dashboard_contrato', id=ordem.contrato.id)
            else:
                return redirect('adicionar_servicos_ordem', ordem_id=ordem.id)
        else:
            messages.error(request, "Erro ao salvar o serviço.")
    else:
        formset = ServicoFormSet(instance=ordem, queryset=Servico.objects.none())

    return render(request, 'ordemservico/adicionar_servicos_ordem.html', {
        'ordem': ordem,
        'formset': formset
    })

@login_required
def editar_servico(request, ordem_id, servico_id):
    ordem = get_object_or_404(OrdemServico, id=ordem_id)
    servico = get_object_or_404(Servico, id=servico_id, ordem=ordem)

    if request.method == 'POST':
        form = ServicoForm(request.POST, instance=servico)
        if form.is_valid():
            form.save()
            messages.success(request, "Serviço atualizado com sucesso.")
            return redirect('ver_ordem_servico', ordem_id=ordem.id)
        else:
            messages.error(request, "Erro ao atualizar o serviço.")
    else:
        form = ServicoForm(instance=servico)

    return render(request, 'ordemservico/editar_servico.html', {
        'ordem': ordem,
        'servico': servico,
        'form': form,
    })

def visualizar_servico(request, ordem_id, servico_id):
    ordem = get_object_or_404(OrdemServico, id=ordem_id)
    servico = get_object_or_404(Servico, id=servico_id, ordem=ordem)

    situacao_choices = Servico._meta.get_field('situacao').choices

    outros_servicos = ordem.servicos.exclude(id=servico.id)

    if request.method == 'POST':
        nova = request.POST.get('situacao')
        if nova in dict(situacao_choices):
            servico.situacao = nova
            servico.save()
        return redirect('visualizar_servico', ordem_id=ordem.id, servico_id=servico.id)

    return render(request, 'ordemservico/visualizar_servico.html', {
        'ordem': ordem,
        'servico': servico,
        'situacao_choices': situacao_choices,
        'outros_servicos': outros_servicos,  # ← Aqui!
    })


def excluir_servico(request, ordem_id, servico_id):
    servico = get_object_or_404(Servico, id=servico_id, ordem__id=ordem_id)
    if request.method == 'POST':
        servico.delete()
        # Redireciona para a visualização da ordem, ou onde preferir
        return redirect('visualizar_ordem', ordem_id=ordem_id)
    # Se quiser, você pode renderizar uma página de confirmação;  
    # mas como já há confirmação em JS, apenas redirecione:
    return redirect('ordemservico/visualizar_servico', ordem_id=ordem_id, servico_id=servico_id)



###########FOTOS###########

@login_required
def listar_albuns(request, ordem_id, servico_id):
    ordem = get_object_or_404(OrdemServico, id=ordem_id)
    servico = get_object_or_404(Servico, id=servico_id, ordem=ordem)
    albuns = servico.albuns.all()
    return render(request, 'ordemservico/adicionar_fotos.html', {
        'ordem': ordem,
        'servico': servico,
        'albuns': albuns
    })

@login_required
def criar_album(request, ordem_id, servico_id):
    servico = get_object_or_404(Servico, id=servico_id, ordem_id=ordem_id)
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            album = form.save(commit=False)
            album.servico = servico
            album.save()
            messages.success(request, "Álbum criado com sucesso.")
            return redirect('listar_albuns', ordem_id=ordem_id, servico_id=servico_id)
    else:
        form = AlbumForm()
    return render(request, 'ordemservico/criar_album.html', {
        'form': form,
        'servico': servico
    })

@login_required
def gerenciar_album(request, ordem_id, servico_id, album_id):
    album = get_object_or_404(Album, id=album_id, servico__id=servico_id, servico__ordem_id=ordem_id)
    if request.method == 'POST':
        form = FotoForm(request.POST, request.FILES)
        if form.is_valid():
            foto = form.save(commit=False)
            foto.album = album
            foto.save()
            messages.success(request, "Foto adicionada com sucesso.")
            return redirect('gerenciar_album', ordem_id=ordem_id, servico_id=servico_id, album_id=album_id)
    else:
        form = FotoForm()

    return render(request, 'ordemservico/gerenciar_album.html', {
        'album': album,
        'form': form,
        'fotos': album.fotos.all()
    })

@login_required
def excluir_foto(request, foto_id):
    foto = get_object_or_404(Foto, id=foto_id)
    album = foto.album
    foto.delete()
    messages.success(request, "Foto excluída.")
    return redirect('gerenciar_album', ordem_id=album.servico.ordem.id, servico_id=album.servico.id, album_id=album.id)

@require_POST
@login_required
def excluir_album(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    ordem_id = album.servico.ordem.id
    servico_id = album.servico.id

    album.delete()
    messages.success(request, "Álbum e suas fotos foram excluídos com sucesso.")

    return redirect('listar_albuns', ordem_id=ordem_id, servico_id=servico_id)