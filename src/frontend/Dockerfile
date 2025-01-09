FROM python:3.9-slim

# Configuração básica
WORKDIR /src

# Instalar dependências do sistema (caso necessário, como libpq-dev, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Criar ambiente virtual
RUN python3 -m venv /venv

# Ativar o ambiente virtual e instalar as dependências
ENV PATH="/venv/bin:$PATH"

# Caso 'st-aggrid' não esteja no requirements.txt, instale-o aqui
RUN pip install st-aggrid

# Instalar o Streamlit e as dependências do requirements.txt
RUN pip install --no-cache-dir streamlit  # Instala Streamlit diretamente
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt  # Instala outras dependências listadas

# Copiar o código da aplicação
COPY . .

# Expor a porta
EXPOSE 8501

# Comando para rodar o streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]