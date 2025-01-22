import cv2

# Chemins des fichiers
prototxt_path = "utils/models/deploy.prototxt"
model_path = "utils/models/mobilenet_iter_73000.caffemodel"


# Chargement du modèle
net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

# Initialisation de la caméra
cap = cv2.VideoCapture(0)  # 0 pour la caméra par défaut

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Prétraitement de l'image
    blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
    net.setInput(blob)

    # Détection
    detections = net.forward()
    
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

    # Affichage
    cv2.imshow("Frame", frame)

    # Sortir avec la touche 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
