from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Colaborador, Setor, Tarefa
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import permission_required

def home(request):
    return render(request, 'managements/dashboards/pages/listar.html')


@permission_required('management.view_tarefa', raise_exception=True)
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
