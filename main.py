import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading
import splitter
import uploader
from tkinter import font as tkfont

class AppComptabilite:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion Paie & Drive")
        self.root.geometry("700x600")
        
        # --- PALETTE DE COULEURS APAISANTE ---
        self.colors = {
            "bg_main": "#F4F7F6",       # Gris-Bleu très pâle (Fond)
            "bg_card": "#FFFFFF",       # Blanc (Zones de contenu)
            "text_primary": "#2C3E50",  # Gris foncé (Texte principal)
            "text_secondary": "#7F8C8D",# Gris moyen (Texte secondaire)
            "accent_1": "#26A69A",      # Vert Teal doux (Bouton 1)
            "accent_2": "#42A5F5",      # Bleu ciel doux (Bouton 2)
            "disabled": "#CFD8DC"       # Gris clair (Bouton désactivé)
        }

        self.root.configure(bg=self.colors["bg_main"])

        # --- POLICES ---
        self.title_font = tkfont.Font(family="Helvetica", size=18, weight="bold")
        self.btn_font = tkfont.Font(family="Helvetica", size=11, weight="bold")
        self.log_font = tkfont.Font(family="Consolas", size=9)

        # === EN-TÊTE ===
        header_frame = tk.Frame(root, bg=self.colors["bg_main"])
        header_frame.pack(pady=(30, 20))

        lbl_title = tk.Label(header_frame, text="📦 Automatisation Paie & Drive", 
                             font=self.title_font, bg=self.colors["bg_main"], fg=self.colors["text_primary"])
        lbl_title.pack()
        
        lbl_subtitle = tk.Label(header_frame, text="Traitement des bulletins et upload sécurisé", 
                                font=("Helvetica", 10), bg=self.colors["bg_main"], fg=self.colors["text_secondary"])
        lbl_subtitle.pack(pady=(5, 0))

        # === CARTE D'ACTIONS (Cadre blanc central) ===
        action_card = tk.Frame(root, bg=self.colors["bg_card"], bd=0, padx=20, pady=20)
        action_card.pack(padx=40, fill="x", pady=10)
        
        # Ombre simulée (bordure légère)
        action_card.configure(highlightbackground="#E0E0E0", highlightthickness=1)

        # Bouton 1
        self.btn_split = tk.Button(action_card, text="1. Sélectionner & Éclater le PDF", 
                                   command=self.start_split_thread, 
                                   font=self.btn_font,
                                   bg=self.colors["accent_1"], fg="white", 
                                   activebackground="#00897B", activeforeground="white",
                                   relief="flat", cursor="hand2", 
                                   padx=15, pady=8, borderwidth=0)
        self.btn_split.pack(fill="x", pady=(0, 10))

        # Bouton 2
        self.btn_upload = tk.Button(action_card, text="2. Uploader vers Google Drive", 
                                    command=self.start_upload_thread, 
                                    font=self.btn_font,
                                    bg=self.colors["disabled"], fg="white",
                                    state=tk.DISABLED,
                                    relief="flat", cursor="arrow",
                                    padx=15, pady=8, borderwidth=0)
        self.btn_upload.pack(fill="x")

        # === ZONE DE LOGS ===
        log_label = tk.Label(root, text="Journal d'activité :", 
                             bg=self.colors["bg_main"], fg=self.colors["text_primary"], 
                             font=("Helvetica", 10, "bold"))
        log_label.pack(padx=40, pady=(20, 5), anchor="w")

        self.log_frame = tk.Frame(root, bg="white", bd=0)
        self.log_frame.pack(padx=40, pady=(0, 30), fill="both", expand=True)
        self.log_frame.configure(highlightbackground="#E0E0E0", highlightthickness=1)

        self.log_area = scrolledtext.ScrolledText(self.log_frame, font=self.log_font, 
                                                  bg="white", fg=self.colors["text_primary"],
                                                  bd=0, padx=10, pady=10,
                                                  selectbackground=self.colors["accent_2"])
        self.log_area.pack(fill="both", expand=True)

    def log(self, message):
        """Ajoute un message dans la zone de texte avec un timestamp simple."""
        self.log_area.insert(tk.END, "• " + message + "\n")
        self.log_area.see(tk.END)

    def start_split_thread(self):
        file_path = filedialog.askopenfilename(filetypes=[("Fichiers PDF", "*.pdf")])
        if not file_path: return
        
        self.btn_split.config(state=tk.DISABLED, bg=self.colors["disabled"], cursor="arrow")
        self.log(f"Traitement démarré : {file_path.split('/')[-1]}")
        
        t = threading.Thread(target=self.run_split, args=(file_path,))
        t.start()

    def run_split(self, file_path):
        success, msg = splitter.spliter_pdf_paie(file_path)
        self.log(msg)
        
        # Réactivation visuelle
        self.btn_split.config(state=tk.NORMAL, bg=self.colors["accent_1"], cursor="hand2")
        
        if success:
            messagebox.showinfo("Succès", "Éclatement terminé.\nVérifiez le dossier de sortie.")
            # Activation du bouton 2 avec la couleur bleue
            self.btn_upload.config(state=tk.NORMAL, bg=self.colors["accent_2"], cursor="hand2")

    def start_upload_thread(self):
        if not messagebox.askyesno("Confirmation", "Avez-vous vérifié les fichiers ?"): return

        self.btn_upload.config(state=tk.DISABLED, bg=self.colors["disabled"], cursor="arrow")
        self.log("Connexion au Drive en cours...")
        
        t = threading.Thread(target=self.run_upload)
        t.start()

    def run_upload(self):
        success, msg = uploader.upload_bulletins()
        self.log(msg)
        # On laisse le bouton 2 désactivé ou on le réactive selon votre préférence
        self.btn_upload.config(state=tk.NORMAL, bg=self.colors["accent_2"], cursor="hand2")
        
        if success:
            messagebox.showinfo("Terminé", "Transfert vers le Cloud terminé avec succès.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppComptabilite(root)
    root.mainloop()