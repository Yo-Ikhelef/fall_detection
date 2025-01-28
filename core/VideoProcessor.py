import cv2

class VideoProcessor:
    def __init__(self, camera_index=0, prototxt_path="models/deploy.prototxt", model_path="models/mobilenet_iter_73000.caffemodel"):
        self.cap = cv2.VideoCapture(camera_index)
        self.net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)  # Chargement du modèle IA
    
    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame
    
    def preprocess_frame(self, frame):
        blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)
        return blob

    def forward(self, blob):
        self.net.setInput(blob)
        detections = self.net.forward()
        return detections


    def release(self):
        self.cap.release()