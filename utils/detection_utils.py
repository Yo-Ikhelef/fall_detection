import cv2
from Camera import Camera
from Detection.UpdateFrame import UpdateFrame
from Detection.Contours import Contours
from Detection.Detections import Detections

# Initialiser la caméra
cam = Camera()

# Initialiser les classes de détection et de gestion de frames
motion_detector = Detections()
frame_updater = UpdateFrame()

try:
    prev_frame = None  # Frame précédente pour la détection de mouvements
    fall_counter = 0

    while True:
        # Obtenir une frame depuis la caméra
        frame = cam.get_frame()

        # Vérifier la détection de mouvement
        movement_detected = motion_detector.movement_detections(frame, prev_frame)

        # Détecter une chute si un mouvement est détecté
        fall_detected = False
        if movement_detected:
            fall_detected = motion_detector.detect_fall(frame, prev_frame)

        if fall_detected:
            fall_counter += 1
            print(f"Chute détectée : {fall_counter}")

        # Dessiner les contours sur l'image actuelle
        instance_contours = Contours(frame)  # Créez une instance pour traiter la frame actuelle
        frame_with_contours = instance_contours.draw_contours(frame)

        # Afficher la vidéo originale avec contours
        cv2.imshow("Vidéo avec contours et mouvement détecté", frame_with_contours)

        # Mettre à jour la frame précédente
        prev_frame = frame

        # Quitter avec 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # Libérer les ressources
    cam.release()
    cv2.destroyAllWindows()
    
