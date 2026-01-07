from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Colaborador, Setor, Tarefa
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from .forms import SetorForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ColaboradorForm


def home(request):
    return render(request, 'managements/dashboards/pages/listar.html')





##############################################################################
####################             SETORES        ##############################
##############################################################################

@permission_required('management.view_setor', raise_exception=True)
def sectors(request):
    setores_list = Setor.objects.all().order_by('nome')
    paginator = Paginator(setores_list, 10)  # 10 linhas por página

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # calcula linhas vazias
    empty_rows = 10 - len(page_obj.object_list)
    if empty_rows < 0:
        empty_rows = 0

    return render(request, 'managements/sectors/pages/listar.html', {
        'page_obj': page_obj,
        'empty_rows': range(empty_rows)
    })

@permission_required('management.add_setor', raise_exception=True)
def setor_create(request):
    if request.method == 'POST':
        form = SetorForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Setor cadastrado com sucesso!')
            return redirect('management:sectors')
    else:
        form = SetorForm()

    return render(request, 'managements/sectors/pages/form.html', {
        'form': form
    })

@permission_required('management.change_setor', raise_exception=True)
def setor_edit(request, id):
    setor = get_object_or_404(Setor, id=id)

    if request.method == 'POST':
        form = SetorForm(request.POST, request.FILES, instance=setor)

        if form.is_valid():
            form.save()
            messages.success(request, 'Setor atualizado com sucesso!')
            return redirect('management:sectors')
    else:
        form = SetorForm(instance=setor)

    return render(request, 'managements/sectors/pages/form.html', {
        'form': form,
        'setor': setor
    })


##############################################################################
####################          COLABORADOR       ##############################
##############################################################################


@permission_required('management.view_tarefa', raise_exception=True)
def colaborators(request):
    colaboradores_list = Colaborador.objects.all().order_by('nome')  # você pode ordenar por algum campo
    paginator = Paginator(colaboradores_list, 10)  # 10 colaboradores por página

    page_number = request.GET.get('page')  # pega o número da página da URL ?page=2
    page_obj = paginator.get_page(page_number)

    # calcular linhas vazias para completar 10 linhas por página
    empty_rows = 10 - len(page_obj.object_list)
    if empty_rows < 0:
        empty_rows = 0

    return render(request, "managements/colaborators/pages/listar.html", {
        "page_obj": page_obj,
        "empty_rows": range(empty_rows)
    })


@permission_required('management.add_colaborador', raise_exception=True)
def colaborador_create(request):
    if request.method == 'POST':
        form = ColaboradorForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Colaborador cadastrado com sucesso!')
            return redirect('management:colaborators')
    else:
        form = ColaboradorForm()

    return render(request, 'managements/colaborators/pages/form.html', {
        'form': form
    })

@permission_required('management.change_colaborador', raise_exception=True)
def colaborador_edit(request, id):
    colaborador = get_object_or_404(Colaborador, id=id)

    if request.method == 'POST':
        form = ColaboradorForm(request.POST, request.FILES, instance=colaborador)

        if form.is_valid():
            form.save()
            messages.success(request, 'Colaborador atualizado com sucesso!')
            return redirect('management:colaborators')
    else:
        form = ColaboradorForm(instance=colaborador)

    return render(request, 'managements/colaborators/pages/form.html', {
        'form': form,
        'colaborador': colaborador
    })



##############################################################################
####################             TAREFAS        ##############################
##############################################################################
@permission_required('management.view_tarefa', raise_exception=True)
def tasks(request):
    tarefas = Tarefa.objects.all().order_by('-data_inicio')

    paginator = Paginator(tarefas, 10)  # 10 linhas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    empty_rows = 10 - len(page_obj.object_list)
    if empty_rows < 0:
        empty_rows = 0

    return render(request, 'managements/tasks/pages/listar.html', {
        'page_obj': page_obj,
        'empty_rows': range(empty_rows),
    })


def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def lista_usuarios(request):
    usuarios = User.objects.all().order_by('username')

    paginator = Paginator(usuarios, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    empty_rows = range(10 - len(page_obj))

    return render(request, 'managements/users/pages/listar.html', {
        'page_obj': page_obj,
        'empty_rows': empty_rows
    })
