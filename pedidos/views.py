from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404

from jogos.models import Jogo
from .models import Pedido, ItemPedido
from .forms import AdicionarAoCarrinhoForm

CARRINHO_SESSAO = 'carrinho'


def _get_carrinho(request):
    return request.session.setdefault(CARRINHO_SESSAO, {})


@login_required
def adicionar_ao_carrinho(request, jogo_id):
    jogo = get_object_or_404(Jogo, pk=jogo_id)

    if request.method == 'POST':
        form = AdicionarAoCarrinhoForm(request.POST)
        if form.is_valid():
            quantidade = form.cleaned_data['quantidade']
            carrinho = _get_carrinho(request)
            chave = str(jogo_id)
            quantidade_atual = carrinho.get(chave, 0)
            nova_quantidade = quantidade_atual + quantidade

            if jogo.tipo_midia == 'fisica' and nova_quantidade > jogo.estoque:
                messages.error(request, f'Estoque insuficiente de "{jogo.nome}".')
            else:
                carrinho[chave] = nova_quantidade
                request.session.modified = True
                messages.success(request, f'"{jogo.nome}" adicionado ao carrinho.')

    return redirect('jogos:detalhe', pk=jogo_id)


@login_required
def ver_carrinho(request):
    carrinho = _get_carrinho(request)
    itens = []
    total = 0

    for jogo_id, quantidade in carrinho.items():
        jogo = get_object_or_404(Jogo, pk=jogo_id)
        subtotal = jogo.preco * quantidade
        total += subtotal
        itens.append({'jogo': jogo, 'quantidade': quantidade, 'subtotal': subtotal})

    return render(request, 'pedidos/carrinho.html', {'itens': itens, 'total': total})


@login_required
def remover_do_carrinho(request, jogo_id):
    carrinho = _get_carrinho(request)
    carrinho.pop(str(jogo_id), None)
    request.session.modified = True
    messages.info(request, 'Item removido do carrinho.')
    return redirect('pedidos:carrinho')


@login_required
def finalizar_pedido(request):
    carrinho = _get_carrinho(request)

    if not carrinho:
        messages.error(request, 'Seu carrinho está vazio.')
        return redirect('pedidos:carrinho')

    pedido = Pedido.objects.create(usuario=request.user)

    try:
        for jogo_id, quantidade in carrinho.items():
            jogo = get_object_or_404(Jogo, pk=jogo_id)
            item = ItemPedido(pedido=pedido, jogo=jogo, quantidade=quantidade, preco_unitario=jogo.preco)
            item.full_clean()
            item.save()
            jogo.baixar_estoque(quantidade)
    except ValidationError as e:
        pedido.delete()
        messages.error(request, f'Não foi possível fechar o pedido: {e.messages[0]}')
        return redirect('pedidos:carrinho')

    request.session[CARRINHO_SESSAO] = {}
    request.session.modified = True
    messages.success(request, 'Pedido fechado com sucesso!')
    return redirect('pedidos:detalhe', pk=pedido.pk)


@login_required
def lista_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user)
    return render(request, 'pedidos/lista.html', {'pedidos': pedidos})


@login_required
def detalhe_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk, usuario=request.user)
    return render(request, 'pedidos/detalhe.html', {'pedido': pedido})


@login_required
def cancelar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk, usuario=request.user)

    if pedido.status != 'pendente':
        messages.error(request, 'Só é possível cancelar pedidos pendentes.')
        return redirect('pedidos:detalhe', pk=pk)

    if request.method == 'POST':
        pedido.status = 'cancelado'
        pedido.save(update_fields=['status'])
        messages.success(request, 'Pedido cancelado.')
        return redirect('pedidos:lista')

    return render(request, 'pedidos/confirmar_cancelamento.html', {'pedido': pedido})