from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome


class Plataforma(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome


class Jogo(models.Model):
    TIPO_MIDIA_CHOICES = [
        ('fisica', 'Física'),
        ('digital', 'Digital'),
    ]

    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    imagem = models.ImageField(upload_to='jogos/', blank=True, null=True)
    categorias = models.ManyToManyField(Categoria, related_name='jogos')
    plataformas = models.ManyToManyField(Plataforma, related_name='jogos')
    tipo_midia = models.CharField(max_length=10, choices=TIPO_MIDIA_CHOICES, default='digital')
    estoque = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nome

    def baixar_estoque(self, quantidade):
        """
        Único ponto de entrada para diminuir o estoque.
        O app "pedidos" chama este método — nunca deve editar
        self.estoque diretamente por fora daqui.
        Ignorado para mídia digital (estoque irrelevante).
        """
        if self.tipo_midia != 'fisica':
            return
        if quantidade > self.estoque:
            raise ValueError('Estoque insuficiente para este jogo.')
        self.estoque -= quantidade
        self.save(update_fields=['estoque'])
