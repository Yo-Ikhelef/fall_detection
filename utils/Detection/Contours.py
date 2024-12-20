import cv2

class Contours: 
    def __init__(self, frame): 
        if frame is None or not hasattr(frame, 'shape'):
            raise ValueError("Invalid frame passed to Contours. Frame cannot be None.")
        
        # Vérifiez si l'image est déjà en niveaux de gris
        if len(frame.shape) == 2:
            self.gray = frame
        else:
            self.gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        self.blurred = cv2.GaussianBlur(self.gray, (5, 5), 0)  # Floutage
        self.edges = cv2.Canny(self.blurred, 30, 100)  # Ajuster les seuils pour Canny
        
    def draw_contours(self, frame): 
        contours, _ = cv2.findContours(self.edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) < 1000:  # Réduire le seuil pour inclure plus de contours
                continue

            # Dessiner les contours et rectangles sur l'image
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        
        return frame
