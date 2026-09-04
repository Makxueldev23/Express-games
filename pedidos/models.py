from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError

from jogos.models import Jogo

    
class Pedido(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('enviado', 'Enviado'),
        ('cancelado', 'Cancelado'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pedidos'
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f'Pedido #{self.pk} - {self.usuario}'

    @property
    def total(self):
        return sum(item.subtotal for item in self.itens.all())


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    jogo = models.ForeignKey(Jogo, on_delete=models.PROTECT, related_name='itens_pedido')
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f'{self.quantidade}x {self.jogo.nome}'

    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def clean(self):
        if self.jogo.tipo_midia == 'fisica' and self.quantidade > self.jogo.estoque:
            raise ValidationError('Estoque insuficiente para este jogo.')

    def save(self, *args, **kwargs):
        if not self.preco_unitario:
            self.preco_unitario = self.jogo.preco
        super().save(*args, **kwargs)