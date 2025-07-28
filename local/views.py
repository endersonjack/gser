from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Local
from .forms import LocalForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages

@login_required
def listar_locais(request):
    locais = Local.objects.all()
    return render(request, 'local/listar_locais.html', {'locais': locais})

@login_required
def inserir_local(request):
    if request.method == 'POST':
        form = LocalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Local inserido com sucesso.')
            return redirect('locais')
        else:
            messages.error(request, 'Erro ao inserir. Verifique os dados.')
    else:
        form = LocalForm()
    return render(request, 'local/inserir_local.html', {'form': form})


@login_required
def editar_local(request, local_id):
    local = get_object_or_404(Local, id=local_id)
    if request.method == 'POST':
        form = LocalForm(request.POST, instance=local)
        if form.is_valid():
            form.save()
            messages.success(request, 'Local atualizado com sucesso.')
            return redirect('editar_local', local_id=local.id)
        else:
            messages.error(request, 'Erro ao salvar. Verifique os dados informados.')
    else:
        form = LocalForm(instance=local)
    return render(request, 'local/editar_local.html', {'form': form, 'local': local})

@login_required
@require_POST
def excluir_local(request, local_id):
    local = get_object_or_404(Local, id=local_id)
    local.delete()
    messages.success(request, 'Local excluído com sucesso.')
    return redirect('locais')