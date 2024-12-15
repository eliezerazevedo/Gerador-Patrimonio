# Use uma imagem base oficial do Python
FROM python:3.12-slim

# Instalar dependências para fusos horários
RUN apt-get update && apt-get install -y tzdata

# Instalar dependências para compilar Pillow
RUN apt-get update && apt-get install -y \
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

# Copie o arquivo requirements.txt para dentro do container
COPY requirements.txt .

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie todo o código da aplicação para dentro do container
COPY . .

# Exponha a porta que a aplicação Flask vai rodar
EXPOSE 5997

# Comando para rodar a aplicação Flask
CMD ["python", "app.py"]