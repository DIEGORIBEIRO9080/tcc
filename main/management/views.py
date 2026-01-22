from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Colaborador, Setor, Tarefa
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from .forms import *
from django.shortcuts import render, redirect, get_object_or_404




import csv
import json
from datetime import datetime
from django.http import HttpResponse
from django.db.models import Q
from openpyxl import Workbook
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors







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


@permission_required('management.view_colaborador', raise_exception=True)
def colaborators(request):

    status_selecionados = request.GET.getlist('status')

    colaboradores_list = Colaborador.objects.all().order_by('nome')  # você pode ordenar por algum campo
    

    
    if status_selecionados:
        colaboradores_list = colaboradores_list.filter(
            status__in=status_selecionados
        )

    page_number = request.GET.get('page')  # pega o número da página da URL ?page=2
    paginator = Paginator(colaboradores_list, 10)  # 10 colaboradores por página
    page_obj = paginator.get_page(page_number)
    
    # calcular linhas vazias para completar 10 linhas por página
    empty_rows = 10 - len(page_obj.object_list)
    if empty_rows < 0:
        empty_rows = 0

    return render(request, "managements/colaborators/pages/listar.html", {
        "page_obj": page_obj,
        "empty_rows": range(empty_rows),
        'status_selecionados': status_selecionados,
    })

@permission_required('management.change_colaborador', raise_exception=True)
def colaborador_mudar_status(request, id, novo_status):
    colaborador = get_object_or_404(Colaborador, id=id)

    status_validos = ['ativo', 'ferias', 'desligado']

    if novo_status not in status_validos:
        messages.error(request, 'Status inválido.')
        return redirect('management:colaborators')

    colaborador.status = novo_status
    colaborador.save()

    messages.success(
        request,
        f'Status de {colaborador.nome} alterado para {colaborador.get_status_display()}'
    )

    return redirect('management:colaborators')


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
    status_selecionados = request.GET.getlist('status')

    tarefas = Tarefa.objects.all().order_by('-data_inicio')

    if status_selecionados:
        tarefas = tarefas.filter(status__in=status_selecionados)

    paginator = Paginator(tarefas, 10)  # 10 linhas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    empty_rows = 10 - len(page_obj.object_list)
    if empty_rows < 0:
        empty_rows = 0

    return render(request, 'managements/tasks/pages/listar.html', {
        'page_obj': page_obj,
        'empty_rows': range(empty_rows),
        'status_selecionados': status_selecionados,
    })
@permission_required('management.change_tarefa', raise_exception=True)
def alterar_status_tarefa(request, tarefa_id, novo_status):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)

    # validação extra (segurança)
    status_validos = ['pendente', 'em_andamento', 'concluida', 'cancelada']
    if novo_status not in status_validos:
        messages.error(request, 'Status inválido.')
        return redirect('management:tasks')

    tarefa.status = novo_status
    tarefa.save()

    messages.success(request, 'Status da tarefa atualizado com sucesso!')
    return redirect('management:tasks')

@permission_required('management.add_tarefa', raise_exception=True)
def tarefa_create(request):
    if request.method == 'POST':
        form = TarefaForm(request.POST, request.FILES)

        if form.is_valid():
            tarefa= form.save()

            setores = form.cleaned_data['setores']
            colaboradores = form.cleaned_data['colaboradores']

            tarefa.setores.set(setores)  # Django cuida do through
            tarefa.colaboradores.set(colaboradores)
            

            messages.success(request, 'tarefa cadastrado com sucesso!')
            return redirect('management:tasks')
    else:
        form = TarefaForm()

    return render(request, 'managements/tasks/pages/form.html', {
        'form': form
    })

@permission_required('management.change_tarefas', raise_exception=True)
def tarefa_edit(request, id):
    tarefa = get_object_or_404(Tarefa, id=id)

    if request.method == 'POST':
        form = TarefaForm(request.POST, request.FILES, instance=tarefa)

        if form.is_valid():
            form.save()
            messages.success(request, 'tarefa atualizada com sucesso!')
            return redirect('management:tasks')
    else:
        form = TarefaForm(instance=tarefa)

    return render(request, 'managements/tasks/pages/form.html', {
        'form': form,
        'tarefa': tarefa
    })











##############################################################################
####################            USUARIOS        ##############################
##############################################################################
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






@permission_required('management.view_tarefa', raise_exception=True)
def relatorio_form(request):
    setores = Setor.objects.all()
    colaboradores = Colaborador.objects.all()

    context = {
        'setores': setores,
        'colaboradores': colaboradores,
    }
    return render(request, 'managements/reports/pages/form.html', context)


from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.http import HttpResponse
from .models import Tarefa, Setor, Colaborador
from openpyxl import Workbook
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import csv
import json

@permission_required('management.view_tarefa', raise_exception=True)
def gerar_relatorio(request):
    # ====== PEGAR FILTROS ======
    setores = request.GET.getlist('setores')
    colaboradores = request.GET.getlist('colaboradores')
    status = request.GET.get('status')
    prioridade = request.GET.get('prioridade')
    nivel_sujeira = request.GET.get('nivel_sujeira')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    formato = request.GET.get('formato', 'csv')

    # ====== QUERY BASE ======
    tarefas_query = Tarefa.objects.all()

    # ====== APLICAR FILTROS ======
    if setores:
        tarefas_query = tarefas_query.filter(setores__id__in=setores).distinct()
    
    if colaboradores:
        tarefas_query = tarefas_query.filter(colaboradores__id__in=colaboradores).distinct()
    
    if status:
        tarefas_query = tarefas_query.filter(status=status)
    
    if prioridade:
        tarefas_query = tarefas_query.filter(prioridade=prioridade)
    
    if nivel_sujeira:
        tarefas_query = tarefas_query.filter(nivel_sujeira=nivel_sujeira)
    
    if data_inicio:
        tarefas_query = tarefas_query.filter(data_inicio__gte=data_inicio)
    
    if data_fim:
        tarefas_query = tarefas_query.filter(data_termino__lte=data_fim)

    tarefas = tarefas_query.prefetch_related('setores', 'colaboradores')
    total_registros = tarefas.count()

    # ====== Preparar dados ======
    cabecalho = [
        "ID", "Tarefa", "Descrição", "Status", "Prioridade",
        "Nível de Sujeira", "Setores", "Colaboradores",
        "Data Início", "Data Previsão Término", "Data Término"
    ]
    dados = []
    for t in tarefas:
        setores_nome = ", ".join([s.nome for s in t.setores.all()])
        colaboradores_nome = ", ".join([c.nome for c in t.colaboradores.all()])
        dados.append([
            t.id,
            t.titulo,
            t.descricao,
            t.get_status_display(),
            t.get_prioridade_display(),
            t.get_nivel_sujeira_display(),
            setores_nome,
            colaboradores_nome,
            t.data_inicio.strftime('%d/%m/%Y') if t.data_inicio else "",
            t.data_previsao_termino.strftime('%d/%m/%Y') if t.data_previsao_termino else "",
            t.data_termino.strftime('%d/%m/%Y') if t.data_termino else ""
        ])

    # ====== EXPORTAÇÃO ======
    if formato == 'csv':
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="relatorio_tarefas_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        response.write('\ufeff')  # BOM para Excel
        writer = csv.writer(response, delimiter=';')
        writer.writerow(cabecalho)
        for linha in dados:
            writer.writerow(linha)
        return response

    elif formato == 'xlsx':
        wb = Workbook()
        ws = wb.active
        ws.title = "Relatório de Tarefas"
        ws.append(cabecalho)
        for linha in dados:
            ws.append(linha)
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="relatorio_tarefas_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx"'
        wb.save(response)
        return response

    elif formato == 'json':
        lista = []
        for t in tarefas:
            lista.append({
                "id": t.id,
                "titulo": t.titulo,
                "descricao": t.descricao,
                "status": t.get_status_display(),
                "prioridade": t.get_prioridade_display(),
                "nivel_sujeira": t.get_nivel_sujeira_display(),
                "setores": [s.nome for s in t.setores.all()],
                "colaboradores": [c.nome for c in t.colaboradores.all()],
                "data_inicio": t.data_inicio.strftime('%d/%m/%Y') if t.data_inicio else "",
                "data_previsao_termino": t.data_previsao_termino.strftime('%d/%m/%Y') if t.data_previsao_termino else "",
                "data_termino": t.data_termino.strftime('%d/%m/%Y') if t.data_termino else ""
            })
        return HttpResponse(json.dumps(lista, indent=4, ensure_ascii=False), content_type="application/json; charset=utf-8")

    # Render template
    context = {
        'tarefas': tarefas,
        'setores': Setor.objects.all(),
        'colaboradores': Colaborador.objects.all(),
        'total_registros': total_registros
    }
    return render(request, 'managements/reports/pages/form.html', context)
