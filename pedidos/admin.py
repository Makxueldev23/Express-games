from django.contrib import admin
from .models import Pedido, ItemPedido


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'status', 'criado_em', 'total']
    inlines = [ItemPedidoInline]