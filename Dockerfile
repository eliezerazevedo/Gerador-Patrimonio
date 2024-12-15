# Usar imagem base do Python
FROM python:3.12-slim

# Definir variáveis de ambiente para evitar que o Python gere arquivos de bytecode e para o pip não usar cache
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_NO_CACHE_DIR=1

# Criar um diretório de trabalho no contêiner
WORKDIR /app

# Copiar o arquivo de dependências
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação para dentro do contêiner
COPY . .

# Criar um usuário não-root para executar a aplicação de maneira mais segura
RUN useradd -m appuser
USER appuser

# Expor a porta que o Flask utiliza
EXPOSE 5997

# Definir o comando para rodar a aplicação
CMD ["python", "app.py"]
