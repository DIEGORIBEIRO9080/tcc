from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import LoginForm

@login_required()
def register_view(request):
    form = RegisterForm()  # SEM request.POST
    

    return render(request, 'authors/cadastro/index.html', {'form': form})

@login_required()
def register_create(request):
    if request.method != "POST":
        return redirect('authors:usuarios_cadastrar')

    form = RegisterForm(request.POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()

        role = form.cleaned_data['role']

        if role == 'Admin':
            user.is_superuser = True
            user.is_staff = True
            user.save()
        else:
            grupo, _ = Group.objects.get_or_create(name=role)
            user.groups.add(grupo)

        messages.success(request, "Usuário criado com sucesso!")

        # 🔥 volta pro formulário limpo e mostra mensagem
        form = RegisterForm()
        return redirect('management:lista_usuarios')

    messages.error(request, "Erro ao cadastrar usuário. Verifique os campos.")
    return render(request, 'authors/cadastro/index.html', {'form': form})





@login_required()
def user_edit_view(request, user_id):
    user = get_object_or_404(User, id=user_id)

    role_atual = user.groups.first().name if user.groups.exists() else "Leitor"

    form = RegisterForm(instance=user, initial={"role": role_atual})

    

    return render(request, "authors/cadastro/index.html", {
        "form": form,
        "edit_user": user
    })


@login_required()
def user_edit_save(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method != "POST":
        return redirect("authors:user_edit", user_id=user.id)

    form = RegisterForm(request.POST, instance=user)

    if form.is_valid():
        user = form.save(commit=False)

        # Atualiza senha apenas se preenchida
        password = form.cleaned_data.get("password")
        if password:
            user.set_password(password)

        user.save()

        # Atualiza permissões
        role = form.cleaned_data["role"]
        user.groups.clear()

        if role == "Admin":
            user.is_superuser = True
            user.is_staff = True
        else:
            user.is_superuser = False
            user.is_staff = False
            grupo, _ = Group.objects.get_or_create(name=role)
            user.groups.add(grupo)

        user.save()

        messages.success(request, "Usuário atualizado com sucesso!")

        # ✅ REDIRECIONAMENTO CORRETO
        return redirect("management:lista_usuarios")

    messages.error(request, "Erro ao atualizar usuário. Verifique os campos.")

    return render(request, "authors/cadastro/index.html", {
        "form": form,
        "edit_user": user
    })


@login_required()
@permission_required('auth.delete_user', raise_exception=True)
def user_delete(request, id):

    user = get_object_or_404(User, id=id)

    if request.method != "POST":
        return redirect('/usuarios/')

    # 🚫 não excluir o usuário logado
    if request.user.id == user.id:
        messages.error(request, "Você não pode excluir o usuário que está logado.")
        return redirect('/usuarios/')

    user.delete()
    messages.success(request, "Usuário excluído com sucesso!")

    return redirect('/usuarios/')

from django.contrib.auth import logout



def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, f"Bem-vindo, {user.first_name}!")
            # ✅ Redireciona para a página inicial do projeto
            return redirect('management:home')  
        else:
            messages.error(request, "Usuário ou senha incorretos.")

    return render(request, 'authors/cadastro/logar.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "Você saiu com sucesso!")
    return redirect('authors:login')  # URL fixa para login
