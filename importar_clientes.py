import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao.settings')
django.setup()

from tarefas.models import Cliente

arquivo = "contatos.csv"

importados = 0
ignorados = 0

with open(arquivo, "r", encoding="utf-8", errors="ignore") as f:
    linhas = f.readlines()

for linha in linhas:
    linha = linha.strip()

    if not linha or linha.startswith("NOME"):
        continue

    # tenta pegar email dentro de <>
    match_email = re.search(r'<([^>]+)>', linha)

    if match_email:
        email = match_email.group(1)
        nome = linha.split("<")[0].replace('"', '').strip()
    else:
        partes = linha.split(",")
        nome = partes[0].strip()
        email = ""

    if not nome:
        ignorados += 1
        continue

    if Cliente.objects.filter(nome=nome, email=email).exists():
        ignorados += 1
        continue

    Cliente.objects.create(
        nome=nome,
        telefone="",
        email=email,
        observacoes="Importado arquivo bagunçado"
    )

    importados += 1

print("Importação concluída!")
print(f"Clientes importados: {importados}")
print(f"Contatos ignorados: {ignorados}")