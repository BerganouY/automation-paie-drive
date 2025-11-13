import os

# === CONFIGURATION LOCALE ===
OUTPUT_DIR = "output_bulletins"
LOG_DIR = "logs"

# === CONFIGURATION GOOGLE DRIVE ===
# Remplacez ceci par l'ID du dossier "Salariés" sur votre Google Drive.
# L'ID est la partie alphanumérique à la fin de l'URL du dossier.
# Ex: drive.google.com/drive/folders/1A2B3C4D5E6F7G8H9I0J
DRIVE_PARENT_FOLDER_ID = "1YiPrag7loAhwuLOxWeKhzgtfPqSLfGsT"

# Chemins absolus pour éviter les erreurs
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(BASE_DIR, 'credentials.json')
TOKEN_FILE = os.path.join(BASE_DIR, 'token.json')