from django.db import models
from django.contrib.auth.models import User


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
        ('pendente', 'Pendente'),
        ('andamento', 'Em andamento'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    ]

    TIPOS_SERVICO = [
        ('instalacao', 'Instalação'),
        ('manutencao', 'Manutenção'),
        ('limpeza', 'Limpeza'),
        ('reparo', 'Reparo'),
        ('vistoria', 'Vistoria'),
    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='servicos'
    )

    tipo_servico = models.CharField(
        max_length=20,
        choices=TIPOS_SERVICO,
        blank=True,
        null=True,
        verbose_name='Tipo de Serviço'
    )

    descricao = models.TextField()
    defeito_relatado = models.TextField(blank=True, null=True)
    diagnostico = models.TextField(blank=True, null=True)

    data_servico = models.DateField()

    # 👉 NOVOS CAMPOS (AQUI É O LUGAR CERTO)
    data_agendada = models.DateField(
        blank=True,
        null=True,
        verbose_name='Data do Agendamento'
    )

    hora_agendada = models.TimeField(
        blank=True,
        null=True,
        verbose_name='Hora do Agendamento'
    )

    valor_cobrado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente'
    )

    documento = models.FileField(
        upload_to='servicos/documentos/',
        blank=True,
        null=True,
        verbose_name='Documento'
    )

    imagem = models.ImageField(
        upload_to='servicos/imagens/',
        blank=True,
        null=True,
        verbose_name='Imagem'
    )

    def total_despesas(self):
        return sum(d.valor for d in self.despesas.all())

    def lucro(self):
        return self.valor_cobrado - self.total_despesas()

    def __str__(self):
        return f"Serviço #{self.id} - {self.cliente.nome}"

class Despesa(models.Model):
    servico = models.ForeignKey(
        'Servico',
        on_delete=models.CASCADE,
        related_name='despesas'
    )
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor}"


ACAO_CHOICES = [
    ('criou', 'Criou'),
    ('alterou', 'Alterou'),
    ('deletou', 'Deletou'),
    ('login', 'Login'),
    ('logout', 'Logout'),
]


class LogAuditoria(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    nome_usuario = models.CharField(max_length=150, blank=True)
    acao = models.CharField(max_length=20, choices=ACAO_CHOICES)
    modelo = models.CharField(max_length=100)
    objeto_id = models.PositiveIntegerField()
    descricao = models.TextField(blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.data} - {self.nome_usuario} - {self.acao}"