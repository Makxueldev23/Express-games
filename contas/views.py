from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import CadastroForm, EditarPerfilForm


def cadastro(request):
    if request.user.is_authenticated:
        return redirect('contas:perfil')

    if request.method == 'POST':
        form = CadastroForm(request.POST)

        if form.is_valid():
            user = form.save()

            messages.success(
                request,
                'Cadastro realizado com sucesso!'
            )

            login(request, user)

            return redirect('contas:perfil')

    else:
        form = CadastroForm()

    return render(
        request,
        'contas/cadastro.html',
        {'form': form}
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect('contas:perfil')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            messages.success(
                request,
                f'Bem-vindo, {user.username}!'
            )

            return redirect('contas:perfil')

        messages.error(
            request,
            'Usuário ou senha incorretos.'
        )

    return render(
        request,
        'contas/login.html'
    )


@login_required
def logout_view(request):
    logout(request)

    messages.success(
        request,
        'Você saiu da sua conta.'
    )

    return redirect('contas:login')


@login_required
def perfil(request):
    return render(
        request,
        'contas/perfil.html',
        {'usuario': request.user}
    )


@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = EditarPerfilForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Perfil atualizado com sucesso!'
            )

            return redirect('contas:perfil')

    else:
        form = EditarPerfilForm(
            instance=request.user
        )

    return render(
        request,
        'contas/editar_perfil.html',
        {'form': form}
    )
