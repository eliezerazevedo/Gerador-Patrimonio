# Use uma imagem base oficial do Python
FROM python:3.13.1-slim

# Configurações de ambiente para melhor desempenho e menor ruído
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Instalar dependências necessárias em uma única etapa
RUN apt-get update && apt-get install -y --no-install-recommends \
    tzdata \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    tcl8.6-dev \
    tk8.6-dev \
    && rm -rf /var/lib/apt/lists/*

# Defina o diretório de trabalho
WORKDIR /app

# Copie e instale as dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código da aplicação
COPY . .

# Exponha a porta da aplicação
EXPOSE 5997

# Comando para rodar a aplicação
CMD ["python", "app.py"]
