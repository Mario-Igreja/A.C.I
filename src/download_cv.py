from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials
import os

# Define os escopos necessários
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

# Carrega as credenciais a partir do arquivo token.json
creds = Credentials.from_authorized_user_file('token.json', SCOPES)

# Constrói o serviço da API do Google Drive
service = build('drive', 'v3', credentials=creds)

# ID da pasta que você deseja listar os arquivos
folder_id = '1ET2yIIUlHDqvkwLXNXqYRyPS3lWhz-_0'

# Listar arquivos na pasta especificada pelo folder_id
results = service.files().list(
    q=f"'{folder_id}' in parents", 
    fields="files(id, name)"
).execute()

# Obter a lista de arquivos
files = results.get('files', [])

if not files:
    raise FileNotFoundError('No files found.')
else:
    print('Files:')
    for file in files:
        print(f"{file['name']} ({file['id']})")

        # Definindo o caminho de onde salvar o arquivo
        file_path = f"./curriculos/{file['name']}"

        # Verifica se o diretório existe, se não, cria
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Download de cada arquivo no drive
        request = service.files().get_media(fileId=file['id'])
        with open(file_path, 'wb') as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}%.")
