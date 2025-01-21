import cv2
from datetime import datetime
from collections import deque


def detect_motion(frame, prev_frame, threshold=50, min_motion_pixels=5000):
    """
    Détecte les mouvements significatifs entre deux frames.
    """
    if prev_frame is None:
        return False
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(prev_gray, gray)
    _, thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
    motion_pixels = cv2.countNonZero(thresh)
    print(f"Pixels en mouvement : {motion_pixels}")  # Débogage
    return motion_pixels > min_motion_pixels


def initialize_video_writer(filename, frame_width, frame_height, fps, codec='avc1'):
    fourcc = cv2.VideoWriter_fourcc(*codec)
    return cv2.VideoWriter(filename, fourcc, fps, (frame_width, frame_height))

def main():
    # Configuration
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Erreur : Impossible d'accéder à la caméra.")
        return

    fps = int(camera.get(cv2.CAP_PROP_FPS)) or 30
    frame_width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"FPS : {fps}, Largeur : {frame_width}, Hauteur : {frame_height}")


    # Tampon circulaire pour les 5 dernières secondes
    buffer = deque(maxlen=fps * 5)
    recording = False
    output = None
    idle_time = 0
    prev_frame = None  # Frame précédente pour la détection de mouvement

    while True:
        ret, frame = camera.read()
        if not ret:
            print("Erreur : Impossible de lire la caméra.")
            break

        # Ajouter la frame au tampon circulaire
        buffer.append(frame)

        # Détecter un mouvement (exemple simplifié)
        motion_detected = detect_motion(frame, prev_frame, threshold=50, min_motion_pixels=5000)

        if motion_detected:
            print("Mouvement détecté !")
            idle_time = 0
            if not recording:
                # Démarrer l'enregistrement avec le contenu du tampon
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"motion_{timestamp}.mp4"
                output = initialize_video_writer(output_filename, frame_width, frame_height, fps)
                for buffered_frame in buffer:
                    output.write(buffered_frame)
                print(f"Enregistrement démarré : {output_filename}")
                recording = True
        elif recording:
            idle_time += 1
            if idle_time > fps * 5:  # Si aucun mouvement pendant 5 secondes
                output.release()
                print("Enregistrement arrêté.")
                recording = False
        

        # Enregistrer si enregistrement actif
        if recording:
            output.write(frame)

        # Mettre à jour prev_frame pour la prochaine itération
        prev_frame = frame.copy()
        
        # Afficher le flux vidéo
        cv2.imshow("Flux Vidéo", frame)

        # Quittez avec 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    if recording:
        output.release()
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
