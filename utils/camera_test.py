import cv2

def main():
    # Initialiser la caméra (0 pour la caméra par défaut, 1 pour une caméra externe, etc.)
    camera = cv2.VideoCapture(0)
    
    # Vérifiez si la caméra est accessible
    if not camera.isOpened():
        print("Erreur : Impossible d'accéder à la caméra.")
        return

    print("Caméra démarrée. Appuyez sur 'q' pour quitter.")

    while True:
        # Lire une image depuis la caméra
        ret, frame = camera.read()
        
        # Vérifiez si la capture est réussie
        if not ret:
            print("Erreur : Impossible de lire la caméra.")
            break

        # Afficher l'image capturée
        cv2.imshow("Flux Vidéo", frame)

        # Quittez avec la touche 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libérez la caméra et fermez les fenêtres
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
