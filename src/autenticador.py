# Importa as bibliotecas necessárias para o fluxo de autenticação OAuth 2.0
from google_auth_oauthlib.flow import InstalledAppFlow  # Para gerenciar o fluxo de autenticação
from google.auth.transport.requests import Request  # Para fazer solicitações HTTP para atualização de credenciais
from google.oauth2.credentials import Credentials  # Para gerenciar as credenciais de acesso
import os.path  # Para manipulação de caminhos e verificação de arquivos

# Define os escopos de acesso que a aplicação irá solicitar
SCOPES = [
    "https://www.googleapis.com/auth/drive.file",        # Permissão para criar e modificar arquivos no Google Drive
    "https://www.googleapis.com/auth/drive.readonly",    # Permissão para ler arquivos no Google Drive
    "https://www.googleapis.com/auth/drive.metadata.readonly"  # Permissão para ler metadados dos arquivos no Google Drive
]

# Inicializa a variável de credenciais
creds = None

# Verifica se o arquivo token.json existe
if os.path.exists('token.json'):
    # Carrega as credenciais a partir do arquivo token.json se ele existir
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    print('Credenciais carregadas do arquivo token.json.')

# Verifica se as credenciais são válidas ou se estão expiradas
if not creds or not creds.valid:
    # Se as credenciais existem mas estão expiradas e podem ser renovadas
    if creds and creds.expired and creds.refresh_token:
        # Renova as credenciais usando o refresh token
        creds.refresh(Request())
        print('Credenciais renovadas com sucesso.')
    else:
        # Inicia o fluxo de autorização do OAuth se não houver credenciais válidas
        print('Iniciando o fluxo de autorização do OAuth...')
        # Cria o fluxo de autenticação usando o arquivo de credenciais
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        # Executa o servidor local para autorização e aguarda a entrada do usuário
        creds = flow.run_local_server(port=41712)  # Certifique-se de usar a mesma porta que você registrou
        print('Autorização concluída.')

    # Salva as credenciais renovadas ou novas no arquivo token.json
    with open('token.json', 'w') as token:
        # Salva as credenciais em formato JSON
        token.write(creds.to_json())
        print('Credenciais salvas no arquivo token.json.')
