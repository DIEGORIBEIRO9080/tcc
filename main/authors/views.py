from django.shortcuts import render, redirect
from.forms import RegisterForm
from django.http import Http404
from django.contrib import messages


def register_view(request):

    form= RegisterForm()

    return render(request, 'authors/cadastro/index.html', {'form':form, }  )

def register_create(request):
    if not request.post:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        form.save()
        messages.success(request, ' você criou um usuario')

        del(request.session['register_form_data'])

    return redirect('authors:cadastrar')
