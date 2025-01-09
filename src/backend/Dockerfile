FROM python:3.9-slim

# Configuração básica
WORKDIR /src

# Copiar e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Porta e comando de inicialização
EXPOSE 8505
CMD ["python", "app.py"]
