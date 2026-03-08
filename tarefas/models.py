from django.db import models


class Cliente(models.Model):
    nome = models.CharField(max_length=150)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nome


class Servico(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    descricao = models.TextField()
    data_servico = models.DateField()
    valor_cobrado = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def total_despesas(self):
        return sum(d.valor for d in self.despesas.all())

    def lucro(self):
        return self.valor_cobrado - self.total_despesas()

    def __str__(self):
        return f"Serviço #{self.id} - {self.cliente}"


class Despesa(models.Model):
    servico = models.ForeignKey(
        Servico,
        on_delete=models.CASCADE,
        related_name='despesas'
    )
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor}"

