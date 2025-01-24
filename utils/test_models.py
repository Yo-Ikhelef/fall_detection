import cv2
'''
# = intégration de l'ia dans le code
## = détection de mouvement
### = détection de chute
#### = enregistrement vidéo
'''

# Chemins des fichiers
prototxt_path = "utils/models/deploy.prototxt"
model_path = "utils/models/mobilenet_iter_73000.caffemodel"


# Chargement du modèle
net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

# Initialisation de la caméra
cap = cv2.VideoCapture(0)  # 0 pour la caméra par défaut

# Configuration pour l'enregistrement vidéo
fourcc = cv2.VideoWriter_fourcc(*"MJPG")
output_file = None
recording = False
recording_timeout = 100  # Nombre de frames après la dernière détection avant l'arrêt de l'enregistrement
recording_counter = 0  # Compteur de frames enregistrées depuis la dernière détection

## Variables pour la détection de mouvement
previous_frame = None
motion_threshold = 5000  ## Seuil pour détecter un mouvement significatif

### Variables pour la détection de chute
fall_threshold = 0.1  # Réduction de hauteur de 10% cumulé sur le nombre de frame de confirm_fall_frames considérée comme une chute
person_heights = {}  # Dictionnaire pour stocker les hauteurs précédentes des individus
fall_frames = {}  # Comptage des frames où une chute est suspectée
fall_buffer = {}  # Buffer pour éviter les multiples déclenchements

### Seuil pour confirmer une chute (nombre d'images consécutives avec une réduction de hauteur)
confirm_fall_frames = 2

### Durée du buffer (en frames) avant de détecter une nouvelle chute
fall_buffer_duration = 10

while True:
    ret, frame = cap.read()
    if not ret:
        break

    

    ## Conversion en niveaux de gris pour la détection de mouvement
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    ## Détection de mouvement
    motion_detected = False
    if previous_frame is not None:
        frame_diff = cv2.absdiff(previous_frame, gray_frame)
        _, thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)
        motion_pixels = cv2.countNonZero(thresh)

        if motion_pixels > motion_threshold:
            motion_detected = True

    ## Mettre à jour l'image précédente
    previous_frame = gray_frame

    #### Copie de l'image originale pour l'enregistrement
    original_frame = frame.copy()
    #### Prétraitement de l'image pour l'enregistrement
    height_rec, width_rec, _ = original_frame.shape

    # Prétraitement de l'image
    blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
    net.setInput(blob)

    # Détection
    detections = net.forward()

    ### Analyse des résultats
    current_person_ids = []  # Liste des IDs de personnes détectées pour cette frame
    
    # Analyse des résultats
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > 0.5:  # Seulement les détections significatives
            class_id = int(detections[0, 0, i, 1])

            # ID de classe pour les personnes (VOC classes)
            if class_id == 15:  # Classe "person"
                box = detections[0, 0, i, 3:7] * [frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]]
                (startX, startY, endX, endY) = box.astype("int")
                
                # Dessiner une boîte autour de la personne
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                label = f"Person: {confidence:.2f}"
                cv2.putText(frame, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                ### Logique de détection de chute
                # Calculer la hauteur actuelle du rectangle
                height = endY - startY
                current_person_ids.append(i)  # Ajouter l'ID de la personne

                # Comparer avec la hauteur précédente si elle existe
                if i in person_heights:
                    previous_height = person_heights[i]
                    if previous_height > 0:  # Éviter les divisions par zéro
                        height_change = (previous_height - height) / previous_height

                        # Si la réduction de hauteur dépasse le seuil
                        if height_change > fall_threshold:
                            # Vérifier si le buffer pour cette personne est actif
                            if fall_buffer.get(i, 0) == 0:
                                fall_frames[i] = fall_frames.get(i, 0) + 1
                                if fall_frames[i] >= confirm_fall_frames:
                                    print(f"Chute confirmée pour l'individu {i} !")
                                    cv2.putText(frame, "Fall Detected!", (startX, startY - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                                    fall_buffer[i] = fall_buffer_duration  # Activer le buffer
                            else:
                                fall_frames[i] = 0
                        else:
                            fall_frames[i] = 0
                    else:
                        fall_frames[i] = 0

                # Mettre à jour la hauteur actuelle comme la nouvelle hauteur précédente
                person_heights[i] = height

    # Mettre à jour les buffers (réduire leur durée à chaque frame)
    for person_id in list(fall_buffer.keys()):
        if fall_buffer[person_id] > 0:
            fall_buffer[person_id] -= 1
        else:
            del fall_buffer[person_id]

    # Nettoyer les données des individus non détectés
    for person_id in list(person_heights.keys()):
        if person_id not in current_person_ids:
            person_heights.pop(person_id, None)
            fall_frames.pop(person_id, None)
            fall_buffer.pop(person_id, None)

    #### Gestion de l'enregistrement
    if motion_detected:
        recording = True
        recording_counter = 0
        if output_file is None:
            output_file = cv2.VideoWriter("output.avi", fourcc, 20, (width_rec, height_rec))
            print("Enregistrement démarré.")

    if recording:
        output_file.write(original_frame)
        recording_counter += 1

        if recording_counter > recording_timeout:
            recording = False
            output_file.release()
            output_file = None
            print("Enregistrement arrêté.")



    # Affichage
    cv2.imshow("Frame", frame)

    # Sortir avec la touche 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
