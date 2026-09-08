from django import forms
from .models import ItemPedido


class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ['jogo', 'quantidade']


class AdicionarAoCarrinhoForm(forms.Form):
    quantidade = forms.IntegerField(min_value=1, initial=1)