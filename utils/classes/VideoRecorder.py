import cv2

class VideoRecorder:
    def __init__(self, output_path="output.avi", fourcc="MJPG", fps=20, timeout=100):
        self.output_file = None
        self.fourcc = cv2.VideoWriter_fourcc(*fourcc)
        self.fps = fps
        self.recording = False
        self.timeout = timeout
        self.counter = 0
        self.timeout_counter = 0
        self.output_path = output_path

    def start_recording(self, frame_size):
        if not self.recording:
            self.output_file = cv2.VideoWriter(self.output_path, self.fourcc, self.fps, frame_size)
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

    def reset_timeout(self):
        """Réinitialiser le timeout lorsque du mouvement est détecté."""
        self.timeout_counter = 0