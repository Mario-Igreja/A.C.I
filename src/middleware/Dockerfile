FROM python:3.9-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y python3-venv && rm -rf /var/lib/apt/lists/*

# Criar e ativar ambiente virtual
RUN python3 -m venv /venv

# Configurar diretório de trabalho
WORKDIR /src

# Copiar dependências e instalar
COPY requirements.txt .
RUN . /venv/bin/activate && pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Porta e comando de inicialização
EXPOSE 8000
CMD ["/venv/bin/python", "app.py"]
