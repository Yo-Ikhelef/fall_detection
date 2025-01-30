from flask import render_template, send_from_directory, abort
import os

FALLS_DIR = os.path.abspath("recordings/falls") 

def setup_routes(app):
    @app.route('/')
    def home():
        # Récupérer les enregistrements de chute (fall_*)
        fall_recordings = [
                {"id": i+1, "name": f} 
                for i, f in enumerate(sorted(os.listdir(FALLS_DIR), reverse=True))
                if f.startswith("fall_") and f.endswith(".avi")
        ]
        return render_template('index.html', fall_recordings=fall_recordings)
    
    @app.route('/telecharger/<directory>/<filename>')
    def download_video(directory, filename):
        """Télécharge une vidéo depuis le dossier spécifié."""
        if directory == "falls":
            directory_path = FALLS_DIR
        else:
            return abort(403)  # Sécurité : interdiction d'accéder à d'autres dossier

        file_path = os.path.join(directory_path, filename)

        # 🔹 Vérification du fichier et affichage debug
        print(f"Recherche du fichier : {file_path}")
        if os.path.exists(file_path):
            return send_from_directory(directory_path, filename, as_attachment=True)
        return abort(404)  # Page 404 si le fichier n'existe pas
