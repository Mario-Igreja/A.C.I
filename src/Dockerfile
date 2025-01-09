# Use a imagem base do Python
FROM python:3.9-slim

# Instale as dependências do sistema (caso necessário para outras dependências)
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Crie e ative um ambiente virtual dentro do diretório de trabalho
WORKDIR /src
RUN python3 -m venv /src/venv

# Copie o requirements.txt para o contêiner
COPY requirements.txt .

# Instale as dependências no ambiente virtual
RUN /src/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copie o restante do código da aplicação
COPY . .

# Exponha a nova porta (8502)
EXPOSE 8502

# Defina o comando de inicialização
CMD ["/src/venv/bin/streamlit", "run", "app.py", "--server.port=8502", "--server.address=0.0.0.0"]
