# Use a imagem base do Python
FROM python:3.9-slim

# Configuração do diretório de trabalho
WORKDIR /src

# Atualizar o apt-get e instalar rsync
RUN apt-get update && apt-get install -y rsync

# Copiar e instalar dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código-fonte da aplicação e script de sincronização
COPY . .

# Tornar o script de sincronização executável (ajustado para sync_tinydb.sh)
RUN chmod +x sync_tinydb.sh

# Comando de inicialização para executar o script
CMD ["./sync_tinydb.sh"]

