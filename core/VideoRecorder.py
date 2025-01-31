import cv2
import os
import glob
from datetime import datetime
from collections import deque
import threading

class VideoRecorder:
    def __init__(self, output_dir="recordings", fourcc="MJPG", fps=20, timeout=100, max_size_mb=1000, buffer_seconds=5):
        self.output_dir = output_dir
        self.detections_dir = os.path.join(self.output_dir, "detections")
        self.falls_dir = os.path.join(self.output_dir, "falls") 
        self.output_file = None
        self.fourcc = cv2.VideoWriter_fourcc(*fourcc)
        self.fps = fps
        self.recording = False
        self.timeout = timeout
        self.counter = 0
        self.timeout_counter = 0
        self.max_size_mb = max_size_mb
        self.buffer_seconds = buffer_seconds
        self.buffer = deque(maxlen=fps * buffer_seconds)
        self.is_recording_fall = False  # ✅ Flag pour savoir si on enregistre une chute


        # Vérifier si tous les dossiers existent, sinon les créer
        os.makedirs(self.detections_dir, exist_ok=True)  # Crée recordings/detections si absent
        os.makedirs(self.falls_dir, exist_ok=True)  # Crée recordings/falls si absent

        self.output_file = None  # Fichier vidéo actif

    def _generate_filename(self, fall=False):
        """Génère un nom de fichier pour les enregistrements."""
        now = datetime.now()
        timestamp = now.strftime("%d-%m-%Y_%Hh%Mm%Ss")
        folder = self.falls_dir if fall else self.detections_dir
        prefix = "fall_" if fall else "recording_"
        return os.path.join(folder, f"{prefix}{timestamp}.avi")

    def start_recording(self, frame_size):
        if not self.recording and not self.is_recording_fall:
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

    def write_frame(self, frame, motion_detected, fall_detected=False, skip_recording=False):
        """Écrit une frame dans le fichier vidéo si l'enregistrement est actif."""
        self.buffer.append(frame)

        if self.recording and not skip_recording:
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
        files = sorted(
            glob.glob(os.path.join(self.detections_dir, "recording_*.avi")),
            key=os.path.getmtime
        )

        if not files:
            print("Aucun fichier trouvé pour suppression.")
            return

        #Limiter la taille totale
        total_size = sum(os.path.getsize(f) for f in files) / (1024 * 1024)  # Taille en Mo
        while total_size > self.max_size_mb and files:
            os.remove(files.pop(0))
            total_size = sum(os.path.getsize(f) for f in files) / (1024 * 1024)

    def reset_timeout(self):
        """Réinitialiser le timeout lorsque du mouvement est détecté."""
        self.timeout_counter = 0

    def save_fall_clip(self, frame_size, video_processor):
        """Créer un enregistrement spécial pour la chute."""
        if self.is_recording_fall:
            return  # ✅ Évite plusieurs enregistrements simultanés

        self.is_recording_fall = True
        self.stop_recording()  # ✅ Stopper l'enregistrement standard avant

        filename = self._generate_filename(fall=True)
        fall_output = cv2.VideoWriter(filename, self.fourcc, self.fps, frame_size)

        print(f"⚠️ Enregistrement de la chute : {filename}")

        buffer_copy = list(self.buffer)
        for frame in buffer_copy:
            fall_output.write(frame)

        # ✅ Capturer 5 secondes après la chute
        for _ in range(self.fps * self.buffer_seconds):
            frame = video_processor.get_frame()             
            if frame is None:
                break
            fall_output.write(frame)

        fall_output.release()
        self.is_recording_fall = False
        self.buffer.clear()  # ✅ Vider le buffer après utilisation

        print(f"✅ Enregistrement de la chute terminé : {filename}")