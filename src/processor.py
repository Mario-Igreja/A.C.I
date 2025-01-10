import os
import uuid
import logging
import requests
from models.resum import Resum
from models.file import File
from ai import GroqClient
from helper import read_uploaded_file, extract_data_analysis
from database import AnalizadorDatabase

# Configuração de constantes
BACKEND_URL = "http://localhost:8501/analise"

# Inicializar cliente de IA e banco de dados
ai = GroqClient()
database = AnalizadorDatabase()

def process_job(curriculos, job):
    """Processa currículos para uma vaga específica."""
    from csp import CSP  # Importando localmente para evitar importação circular
    
    logging.info(f"Processando currículos para a vaga: {job.get('name')}")
    
    # Inicializar CSP para as verificações de restrições
    csp = CSP()
    
    # Definir as variáveis e domínios para o CSP
    csp.add_variable('experience', ['junior', 'mid', 'senior'])
    csp.add_variable('skills', ['python', 'java', 'c++'])
    
    for path in curriculos:
        try:
            # Verificar se o arquivo de currículo existe
            if not os.path.exists(path):
                logging.warning(f"Arquivo não encontrado: {path}")
                continue

            # Ler o conteúdo do arquivo
            content = read_uploaded_file(path)

            # Gerar resumo, opinião e pontuação com IA
            resum = ai.resume_cv(content)
            opnion = ai.generate_opnion(content, job)
            score = ai.generate_score(resum, job)

            logging.info(f"Resumo gerado para {path}: {resum}")
            logging.info(f"Opinião gerada para {path}: {opnion}")
            logging.info(f"Pontuação calculada para {path}: {score}")

            # Aplicar a lógica de CSP para verificar restrições
            # Por exemplo, verificar se a experiência é 'junior' ou 'mid' ou 'senior'
            csp.add_constraint(lambda assignment: assignment['experience'] == 'junior' or assignment['experience'] == 'senior')
            
            # Obter a solução CSP, se válida
            assignment = csp.backtrack()

            if assignment:
                logging.info(f"Restrição de experiência e habilidades satisfeitas: {assignment}")
                
                # Criar esquemas para armazenamento
                resum_schema = Resum(
                    id=str(uuid.uuid4()),
                    job_id=job.get('id'),
                    content=resum,
                    file=str(path),
                    opnion=opnion,
                )
                file_schema = File(
                    file_id=str(uuid.uuid4()),
                    job_id=job.get('id')
                )

                # Gerar análise adicional
                analysis = extract_data_analysis(resum, resum_schema.job_id, resum_schema.id, score)

                # Inserir no banco de dados
                database.resums.insert(resum_schema.model_dump())
                database.analysis.insert(analysis.model_dump())
                database.files.insert(file_schema.model_dump())

                # Enviar os dados ao backend
                send_to_backend(path, job, resum, score)
            else:
                logging.warning(f"Restrições não satisfeitas para o arquivo {path}. Currículo descartado.")

        except Exception as e:
            logging.error(f"Erro ao processar o arquivo {path} para a vaga {job.get('name')}: {e}", exc_info=True)

def send_to_backend(file_path, job, resum, score):
    """Envia os dados ao backend."""
    data = {
        'file_name': os.path.basename(file_path),
        'job_name': job.get('name'),
        'score': score,
        'resum': resum
    }
    try:
        response = requests.post(BACKEND_URL, json=data)
        if response.status_code == 200:
            logging.info(f"Dados enviados com sucesso para o backend: {response.json()}")
        else:
            logging.warning(f"Erro ao enviar dados para o backend: {response.status_code}")
    except Exception as e:
        logging.error(f"Erro ao conectar ao backend: {e}", exc_info=True)
