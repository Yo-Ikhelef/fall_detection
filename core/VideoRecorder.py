import cv2
import os
import glob
from datetime import datetime


class VideoRecorder:
    def __init__(self, output_dir="recordings", fourcc="MJPG", fps=20, timeout=100, max_size_mb=50):
        self.output_dir = output_dir
        self.output_file = None
        self.fourcc = cv2.VideoWriter_fourcc(*fourcc)
        self.fps = fps
        self.recording = False
        self.timeout = timeout
        self.counter = 0
        self.timeout_counter = 0
        self.max_size_mb = max_size_mb


        # Vérifier si le dossier recordings existe, sinon le créer
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def _generate_filename(self):
        now = datetime.now()
        timestamp = now.strftime("%d-%m-%Y_%Hh%Mm%Ss")
        return os.path.join(self.output_dir, f"recording_{timestamp}.avi")

    def start_recording(self, frame_size):
        if not self.recording:
            filename = self._generate_filename()
            self.output_file = cv2.VideoWriter(filename, self.fourcc, self.fps, frame_size)
            self.recording = True
            self.timeout_counter = 0  # Réinitialiser le compteur de timeout
            print("Recording started")

    def stop_recording(self):
        if self.recording:
            self.output_file.release()
            self.output_file = None
            self.recording = False
            print("Recording stopped")

    def write_frame(self, frame, motion_detected):
        """Écrit une frame dans le fichier vidéo si l'enregistrement est actif."""
        if self.recording:
            self.output_file.write(frame)

            # Si aucun mouvement n'est détecté, incrémenter le timeout
            if not motion_detected:
                self.timeout_counter += 1

                # Arrêter l'enregistrement si le timeout est atteint
                if self.timeout_counter > self.timeout:
                    self.stop_recording()
            else:
                # Réinitialiser le compteur de timeout si mouvement détecté
                self.reset_timeout()

    def cleanup_old_files(self):
        # Supprimer les fichiers les plus anciens pour limiter le nombre
        print("Vérification des fichiers à nettoyer...")  # Étape de débogage
        files = sorted(
            glob.glob(os.path.join(self.output_dir, "recording_*.avi")),
            key=os.path.getmtime
        )

        if not files:
            print("Aucun fichier trouvé pour suppression.")
            return

        #Limiter la taille totale
        total_size = sum(os.path.getsize(f) for f in files) / (1024 * 1024)  # Taille en Mo
        print(f"Taille totale des enregistrements : {total_size:.2f} Mo")
        while total_size > self.max_size_mb and files:
            oldest_file = files.pop(0)
            print(f"Suppression du fichier : {oldest_file}")
            os.remove(files.pop(0))
            total_size = sum(os.path.getsize(f) for f in files) / (1024 * 1024)
            print(f"Taille restante après suppression : {total_size:.2f} Mo")

    def reset_timeout(self):
        """Réinitialiser le timeout lorsque du mouvement est détecté."""
        self.timeout_counter = 0