import cv2

class Camera:
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise Exception(f"Impossible d'ouvrir la caméra avec l'index {camera_index}")

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            raise Exception("Erreur : Impossible de capturer une image depuis la webcam")
        return frame

    def release(self):
        """Libère la caméra."""
        self.cap.release()
        cv2.destroyAllWindows()