from django.db import models


class Cliente(models.Model):
    nome = models.CharField(max_length=150)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    documento = models.CharField(max_length=20, blank=True, null=True, verbose_name="CPF/CNPJ")
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome


class Servico(models.Model):

    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('andamento', 'Em andamento'),
        ('aguardando_peca', 'Aguardando peça'),
        ('concluido', 'Concluído'),
        ('entregue', 'Entregue'),
    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='servicos'
    )

    equipamento = models.CharField(max_length=100, blank=True, null=True)
    marca = models.CharField(max_length=50, blank=True, null=True)
    modelo = models.CharField(max_length=50, blank=True, null=True)

    descricao = models.TextField()
    defeito_relatado = models.TextField(blank=True, null=True)
    diagnostico = models.TextField(blank=True, null=True)

    data_servico = models.DateField()

    valor_cobrado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='aberto'
    )

    def total_despesas(self):
        return sum(d.valor for d in self.despesas.all())

    def lucro(self):
        return self.valor_cobrado - self.total_despesas()

    def __str__(self):
        return f"Serviço #{self.id} - {self.cliente.nome}"


class Despesa(models.Model):

    servico = models.ForeignKey(
        Servico,
        on_delete=models.CASCADE,
        related_name='despesas'
    )

    descricao = models.CharField(max_length=200)

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor}"