import uuid
from helper import get_pdf_paths, read_uploaded_file, extract_data_analysis
from database import AnalizadorDatabase
from ai import GroqClient
from models.resum import Resum
from models.file import File
import requests
import os

# URL do backend (substitua pelo URL correto conforme seu ambiente)
backend_url = "http://localhost:8501/analise"  # Certifique-se de que o serviço 'nginx' está acessível no Docker

# Inicializar a conexão com o banco de dados de análise
database = AnalizadorDatabase()

# Obter as vagas do banco de dados
job = database.get_job_by_name('Vaga de Gestor Comercial de B2B')
if job is None:
    print("Vaga 'Gestor Comercial de B2B' não encontrada no banco de dados.")
    exit()

job_engenheiro = database.get_job_by_name('Vaga de Engenheiro de Software')
if job_engenheiro is None:
    print("Vaga 'Engenheiro de Software' não encontrada no banco de dados.")
    exit()

# Inicializar o cliente de IA para processar os currículos
ai = GroqClient()

# Obter os caminhos dos arquivos PDF contendo os currículos
cv_paths = get_pdf_paths('curriculos')  # Verifique se esse diretório está corretamente mapeado no volume Docker

# Lista de vagas para análise
jobs_to_analyze = [job, job_engenheiro]

# Iterar sobre cada vaga e processar os currículos
for current_job in jobs_to_analyze:
    print(f"Processando currículos para a vaga: {current_job.get('name')}")

    # Iterar sobre cada caminho de arquivo de currículo na lista
    for path in cv_paths:
        try:
            # Verificar se o arquivo existe antes de tentar ler
            if not os.path.exists(path):
                print(f"Arquivo não encontrado: {path}")
                continue
            
            # Ler o conteúdo do arquivo PDF de currículo
            content = read_uploaded_file(path)
            
            # Usar o modelo de IA para resumir o conteúdo do currículo
            resum = ai.resume_cv(content)
            print(f"Resumo do currículo ({path}): {resum}")
            
            # Gerar uma opinião sobre o currículo com base na vaga de emprego
            opnion = ai.generate_opnion(content, current_job)
            print(f"Opinião do currículo ({path}): {opnion}")
            
            # Calcular uma pontuação para o currículo com base no resumo e nos requisitos da vaga
            score = ai.generate_score(resum, current_job)
            print(f"Pontuação do currículo ({path}): {score}")
            
            # Criar uma instância do schema Resum para armazenar os dados do resumo
            resum_schema = Resum(
                id=str(uuid.uuid4()),         # Gerar um UUID único para o ID do resumo
                job_id=current_job.get('id'), # Associar o ID da vaga ao resumo
                content=resum,                # Armazenar o conteúdo do resumo
                file=str(path),               # Armazenar o caminho do arquivo de currículo
                opnion=opnion                 # Armazenar a opinião gerada
            )
            
            # Criar uma instância do schema File para armazenar os dados do arquivo
            file = File(
                file_id=str(uuid.uuid4()),    # Gerar um UUID único para o ID do arquivo
                job_id=current_job.get('id')  # Associar o ID da vaga ao arquivo
            )
            
            # Extrair a análise dos dados utilizando o resumo e informações adicionais
            analysis = extract_data_analysis(resum, resum_schema.job_id, resum_schema.id, score)
            
            # Inserir os dados gerados no banco de dados
            database.resums.insert(resum_schema.model_dump())   # Inserir o resumo no banco de dados
            database.analysis.insert(analysis.model_dump())     # Inserir a análise no banco de dados
            database.files.insert(file.model_dump())            # Inserir os dados do arquivo no banco de dados
            
            # Se necessário, enviar os dados ao backend para processamento adicional
            data = {
                'file_name': os.path.basename(path),  # Nome do arquivo
                'job_name': current_job.get('name'),  # Nome da vaga
                'score': score,                       # Pontuação calculada
                'resum': resum                        # Resumo do currículo
            }
            
            # Realizar a requisição POST ao backend
            response = requests.post(backend_url, json=data)
            if response.status_code == 200:
                print(f"Dados enviados com sucesso para o backend: {response.json()}")
            else:
                print(f"Erro ao enviar dados para o backend: {response.status_code}")
            
        except Exception as e:
            print(f"Erro ao processar o arquivo {path} para a vaga {current_job.get('name')}: {e}") 
