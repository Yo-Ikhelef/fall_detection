import cv2
from collections import deque

from .Contours import Contours

class Detections: 
    def __init__(self, prev_frame=None, buffer_size=5, min_detections=5): 
        self.prev_frame = prev_frame
        self.fall_buffer = deque(maxlen=buffer_size)  # Buffer circulaire
        self.min_detections = min_detections  # Nombre minimum de détections pour confirmer une chute


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

        # Afficher la différence et le seuil
        # cv2.imshow("Différence entre frames", diff)
        # cv2.imshow("Seuil pour détection de mouvement", thresh)

        # Compter les pixels en mouvement
        motion_pixels = cv2.countNonZero(thresh)
        # if motion_pixels > min_motion_pixels:
        #     print(f"Pixels en mouvement : {motion_pixels}")
        
        # Mettre à jour la frame précédente
        self.prev_frame = frame

        # Retourner True si un mouvement significatif est détecté
        return motion_pixels > min_motion_pixels
    
    def detect_fall(self, frame, prev_frame, min_area = 4000 , min_aspect_ratio = 0.3, max_aspect_ratio = 2.5):
        """
        Détecte une chute en analysant les contours entre la frame actuelle et précédente.
        """
        if prev_frame is None:
            print("Aucune frame précédente disponible pour comparaison.")
            return False

        # Extraire les contours pour la frame actuelle
        current_contours = Contours(frame)

        # Réduction du bruit dans les contours
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        edges = cv2.dilate(current_contours.edges, kernel, iterations=1)

        # Analyse des contours pour détecter une chute
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        frame_with_rectangles = frame.copy()
        fall_detected = False

        # print(f"Nombre de contours trouvés : {len(contours)}")
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < min_area:  # Filtrer les petites zones
                continue

            # Calculer les dimensions du rectangle englobant
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = h / float(w)

            # Vérifier si le rectangle correspond aux critères de chute
            if min_aspect_ratio < aspect_ratio < max_aspect_ratio:
                fall_detected = True
                color = (0, 0, 255)  # Rouge pour une chute détectée
                print(f"Contour accepté : Aspect Ratio={aspect_ratio:.2f}, Area={area}, Rect=({x}, {y}, {w}, {h})")
                # Dessiner uniquement les rectangles acceptés
                cv2.rectangle(frame_with_rectangles, (x, y), (x + w, y + h), color, 2)


        # Ajouter le résultat de cette frame au buffer
        self.fall_buffer.append(fall_detected)

        # Forcer un affichage même sans contours valides
        if not contours:
            print("Aucun contour détecté.")
        cv2.imshow("Détection de Chute - Rectangles", frame_with_rectangles)

        # Confirmer une chute si le buffer contient suffisamment de détections consécutives
        confirmed_fall = sum(self.fall_buffer) >= self.min_detections
        if confirmed_fall:
            print(f"Chute confirmée après {self.min_detections} détections consécutives !")
        return confirmed_fall




