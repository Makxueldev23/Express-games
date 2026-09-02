from django import forms
from .models import Jogo

class JogoForm(forms.ModelForm):
    class Meta:
        model = Jogo
        fields = ['nome', 'descricao', 'preco', 'imagem', 'categorias', 'plataformas', 'tipo_midia', 'estoque']