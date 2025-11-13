import os
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import config

# Scopes requis pour lire et écrire dans Drive
SCOPES = ['https://www.googleapis.com/auth/drive']

def get_drive_service():
    """Gère l'authentification Google et retourne le service."""
    creds = None
    if os.path.exists(config.TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(config.TOKEN_FILE, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(config.CREDENTIALS_FILE):
                raise FileNotFoundError("Le fichier 'credentials.json' est introuvable !")
            flow = InstalledAppFlow.from_client_secrets_file(config.CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(config.TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)

def upload_bulletins():
    """Parcourt le dossier output et uploade vers Drive."""
    if not os.path.exists(config.OUTPUT_DIR) or not os.listdir(config.OUTPUT_DIR):
        return False, "Aucun bulletin trouvé dans le dossier de sortie."

    logs = []
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    log_filename = os.path.join(config.LOG_DIR, f"log_upload_{today_str}.md")
    logs.append(f"# Log Upload Google Drive - {datetime.datetime.now()}\n")

    try:
        service = get_drive_service()
        files = [f for f in os.listdir(config.OUTPUT_DIR) if f.endswith('.pdf')]
        
        success_count = 0
        
        for filename in files:
            # Extraction Ref (ex: M1001_Octobre_2025.pdf -> M1001)
            ref_salarie = filename.split('_')[0] 

            # 1. Chercher le dossier du salarié
            query = f"name = '{ref_salarie}' and '{config.DRIVE_PARENT_FOLDER_ID}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
            results = service.files().list(q=query, fields="files(id, name)").execute()
            items = results.get('files', [])

            folder_id = None
            
            if not items:
                # 2. Créer le dossier s'il n'existe pas
                file_metadata = {
                    'name': ref_salarie,
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [config.DRIVE_PARENT_FOLDER_ID]
                }
                folder = service.files().create(body=file_metadata, fields='id').execute()
                folder_id = folder.get('id')
                logs.append(f"- 📂 Dossier créé pour {ref_salarie} (ID: {folder_id})")
            else:
                folder_id = items[0]['id']
                logs.append(f"- 🔍 Dossier trouvé pour {ref_salarie} (ID: {folder_id})")

            # 3. Upload du fichier
            file_path = os.path.join(config.OUTPUT_DIR, filename)
            file_metadata = {
                'name': filename,
                'parents': [folder_id]
            }
            media = MediaFileUpload(file_path, mimetype='application/pdf')
            
            file_drive = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            logs.append(f"  -> 🚀 Uploadé : {filename} (ID: {file_drive.get('id')})")
            success_count += 1

    except Exception as e:
        error_msg = f"Erreur lors de l'upload : {str(e)}"
        logs.append(f"\n🔥 {error_msg}")
        with open(log_filename, "w", encoding="utf-8") as f:
            f.write("\n".join(logs))
        return False, error_msg

    # Écriture des logs
    with open(log_filename, "w", encoding="utf-8") as f:
        f.write("\n".join(logs))

    return True, f"Upload terminé.\nFichiers traités : {success_count}\nLogs : {log_filename}"