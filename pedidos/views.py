from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Pedido, ItemPedido
from .forms import ItemPedidoForm


@login_required
def lista_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user)
    return render(request, 'pedidos/lista.html', {'pedidos': pedidos})


@login_required
def detalhe_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk, usuario=request.user)
    return render(request, 'pedidos/detalhe.html', {'pedido': pedido})


@login_required
def criar_pedido(request):
    if request.method == 'POST':
        form = ItemPedidoForm(request.POST)

        if form.is_valid():
            jogo = form.cleaned_data['jogo']
            quantidade = form.cleaned_data['quantidade']

            pedido = Pedido.objects.create(usuario=request.user)

            item = ItemPedido(pedido=pedido, jogo=jogo, quantidade=quantidade)
            item.full_clean()
            item.save()

            jogo.baixar_estoque(quantidade)

            messages.success(request, 'Pedido criado com sucesso!')
            return redirect('pedidos:detalhe', pk=pedido.pk)
    else:
        form = ItemPedidoForm()

    return render(request, 'pedidos/formulario.html', {'form': form})