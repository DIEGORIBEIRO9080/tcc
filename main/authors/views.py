from django.shortcuts import render, redirect
from.forms import RegisterForm
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.models import Group

def register_view(request):

    request.session['number'] = request.session.get('number', 0) + 1

    form = RegisterForm(request.POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])  # criptografa senha
        user.save()

        role = form.cleaned_data['role']
        if role != 'Admin':
            grupo, _ = Group.objects.get_or_create(name=role)
            user.groups.add(grupo)
        else:
            user.is_superuser = True
            user.is_staff = True
            user.save()

        messages.success(request, f'Usuário criado como {role} com sucesso!')

    return render(request, 'authors/cadastro/index.html', {'form':form, }  )

def register_create(request):
    if request.method != "POST":  # ✅ se não for POST, volta para o formulário
        return redirect('authors:usuarios_cadastrar')

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        form.save()
        messages.success(request, ' você criou um usuario')

        # Limpa os dados da sessão
        if 'register_form_data' in request.session:
            del request.session['register_form_data']

        
        role = form.cleaned_data['role']

        if role == 'Admin':
            user.is_superuser = True
            user.is_staff = True
            user.save()
        else:
            group = Group.objects.get(name=role)
            user.groups.add(group)

    return redirect('authors:usuarios_cadastrar')
