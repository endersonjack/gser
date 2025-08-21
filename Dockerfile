FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive

# Instala as bibliotecas necessárias para o WeasyPrint
RUN apt-get update && apt-get install -y \
    build-essential \
    libcairo2 \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libgdk-pixbuf2.0-0 \
    libglib2.0-0 \
    libffi-dev \
    curl \
    pkg-config \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Cria diretório da aplicação
WORKDIR /app

# Copia e instala os pacotes Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia o restante da aplicação
COPY . .

# Coleta os arquivos estáticos (se necessário)
# RUN python manage.py migrate && python manage.py collectstatic --noinput

# Expõe a porta padrão
EXPOSE 8000

# Inicia o Gunicorn com o WSGI do projeto gser
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn gser.wsgi:application --bind 0.0.0.0:8000"]

