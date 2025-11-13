import os
import re
import datetime
import unicodedata
from pypdf import PdfReader, PdfWriter
import config

def normalize_text(text):
    """
    Nettoie le texte : supprime les accents, met en minuscule 
    et remplace les sauts de ligne par des espaces simples.
    Ex: "Référence Salarié" -> "reference salarie"
    """
    if not text: return ""
    # 1. Décomposition des caractères accentués (NFD)
    text = unicodedata.normalize('NFD', text)
    # 2. On garde uniquement les caractères ASCII (supprime les accents)
    text = "".join([c for c in text if unicodedata.category(c) != 'Mn'])
    # 3. Minuscule et suppression espaces multiples
    text = re.sub(r'\s+', ' ', text.lower()).strip()
    return text

def spliter_pdf_paie(source_pdf_path):
    if not os.path.exists(config.OUTPUT_DIR): os.makedirs(config.OUTPUT_DIR)
    if not os.path.exists(config.LOG_DIR): os.makedirs(config.LOG_DIR)

    logs = []
    count_success = 0
    count_error = 0
    
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    log_filename = os.path.join(config.LOG_DIR, f"log_eclatement_{today_str}.md")

    logs.append(f"# Log Eclatement - {datetime.datetime.now()}\n")
    logs.append(f"Fichier source : {source_pdf_path}\n")

    try:
        reader = PdfReader(source_pdf_path)
        total_pages = len(reader.pages)
        logs.append(f"Total pages détectées : {total_pages}\n")

        for i, page in enumerate(reader.pages):
            raw_text = page.extract_text()
            
            # === NORMALISATION RADICALE ===
            # On transforme le texte brut en texte "plat" sans accents
            clean_text = normalize_text(raw_text)
            
            # === ANALYSE (Sur texte simplifié) ===
            
            # 1. Référence
            # On cherche "reference salarie" suivi optionnellement de ":" ou espace
            # Capture le code alphanumérique qui suit (ex: m1001)
            ref_match = re.search(r"reference salarie\s*[:.]?\s*([a-z0-9]+)", clean_text)
            
            # 2. Date
            # On cherche "periode de paie" suivi du mois (lettres) et année (4 chiffres)
            # Ex: "periode de paie octobre 2025"
            date_match = re.search(r"periode de paie\s*[:.]?\s*([a-z]+)\s+(\d{4})", clean_text)

            if ref_match and date_match:
                # On remet en majuscule pour le nom de fichier final car c'est plus propre
                ref = ref_match.group(1).upper()      
                mois = date_match.group(1).capitalize() 
                annee = date_match.group(2)
                
                filename = f"{ref}_{mois}_{annee}.pdf"
                output_path = os.path.join(config.OUTPUT_DIR, filename)
                
                writer = PdfWriter()
                writer.add_page(page)
                
                with open(output_path, "wb") as out_file:
                    writer.write(out_file)
                
                logs.append(f"- ✅ Page {i+1} : {filename}")
                count_success += 1
            else:
                # Debugging : On affiche ce que le script a "vu" après nettoyage
                logs.append(f"- ❌ Page {i+1} : Échec.")
                logs.append(f"    > Texte nettoyé vu par le script : '{clean_text[:100]}...'")
                count_error += 1

    except Exception as e:
        logs.append(f"\n🔥 ERREUR CRITIQUE : {str(e)}")
        print(f"Erreur: {e}")
        return False, f"Erreur critique : {str(e)}"

    with open(log_filename, "w", encoding="utf-8") as f:
        f.write("\n".join(logs))

    summary = f"Traitement terminé.\nSuccès : {count_success}\nEchecs : {count_error}\nLogs sauvegardés dans {log_filename}"
    return True, summary