from django.db import models

class Projeto(models.Model):
    nome = models.CharField(max_length=120)
    def __str__(self):
        return self.nome

class Responsavel(models.Model):
    nome = models.CharField(max_length=120)
    username = models.CharField(max_length=60, unique=True)
    def __str__(self):
        return f"{self.nome} ({self.username})"

class Tarefa(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    projeto = models.ForeignKey(Projeto, on_delete=models.SET_NULL, null=True, blank=True)
    responsavel = models.ForeignKey(Responsavel, on_delete=models.SET_NULL, null=True, blank=True)
    prazo = models.DateField(null=True, blank=True)
    foto = models.ImageField(upload_to="uploads/", null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo