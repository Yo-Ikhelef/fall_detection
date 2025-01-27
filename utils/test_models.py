import cv2
from classes.VideoProcessor import VideoProcessor
from classes.MotionDetection import MotionDetection
from classes.FallDetection import FallDetection
from classes.VideoRecorder import VideoRecorder

# Initialisation des composants
video_processor = VideoProcessor()
motion_detection = MotionDetection()
fall_detection = FallDetection()
video_recorder = VideoRecorder()

# Chargement du modèle
prototxt_path = "utils/models/deploy.prototxt"
model_path = "utils/models/mobilenet_iter_73000.caffemodel"
net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

while True:
    frame = video_processor.get_frame()
    if frame is None:
        break

    original_frame = frame.copy()

    # Détection de mouvement
    motion_detected = motion_detection.detect_motion(frame)

    # Prétraitement IA
    blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()

    # Récupérer les rectangles à dessiner
    current_person_ids, rectangles = fall_detection.analyze_detection(detections, frame.shape)

    # Dessiner les rectangles sur la frame
    for (startX, startY, endX, endY, confidence) in rectangles:
        cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
        label = f"Person: {confidence:.2f}"
        cv2.putText(frame, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


    # Enregistrement vidéo
    if motion_detected:
        video_recorder.start_recording((frame.shape[1], frame.shape[0]))
        video_recorder.reset_timeout()

    if video_recorder.recording:
        video_recorder.write_frame(original_frame, motion_detected)
        
    # Affichage
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Nettoyage
video_processor.release()
cv2.destroyAllWindows()