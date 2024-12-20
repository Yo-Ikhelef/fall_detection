import cv2
from .Contours import Contours

class Detections: 
    def __init__(self, prev_frame=None): 
        self.prev_frame = prev_frame

    def movement_detections(self, frame, prev_frame, threshold=50, min_motion_pixels=2000): 
    # Vérifier si prev_frame est valide
        if prev_frame is None:
            print("Aucune frame précédente disponible.")
            self.prev_frame = frame  # Initialiser la frame précédente
            return False

        # Obtenir les niveaux de gris pour la frame actuelle et précédente
        prev_gray = Contours(self.prev_frame).gray
        current_gray = Contours(frame).gray

        # Assurez-vous que les deux images ont la même taille
        if prev_gray.shape != current_gray.shape:
            current_gray = cv2.resize(current_gray, (prev_gray.shape[1], prev_gray.shape[0]))

        # Calculer la différence entre les frames
        diff = cv2.absdiff(prev_gray, current_gray).astype("uint8")  # Forcer le type correct
        _, thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)

        # Compter les pixels en mouvement
        motion_pixels = cv2.countNonZero(thresh)
        if motion_pixels > min_motion_pixels:
            print(f"Pixels en mouvement : {motion_pixels}")
        
        # Mettre à jour la frame précédente
        self.prev_frame = frame

        # Retourner True si un mouvement significatif est détecté
        return motion_pixels > min_motion_pixels
