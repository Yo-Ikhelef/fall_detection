import cv2
from picamera2 import Picamera2

class VideoProcessor:
    def __init__(self, camera_index=0, prototxt_path="models/deploy.prototxt", model_path="models/mobilenet_iter_73000.caffemodel"):
        self.picam2 = Picamera2()
        print(Picamera2.global_camera_info())
        self.picam2.configure(self.picam2.create_video_configuration(main={"format": "RGB888", "size": (640, 480)}))
        self.picam2.start()
        self.net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

    def get_frame(self):
        frame = self.picam2.capture_array()
        return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) if frame is not None else None
    
    def preprocess_frame(self, frame):
        return cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)

    def forward(self, blob):
        self.net.setInput(blob)
        detections = self.net.forward()
        return detections


    def release(self):
        self.picam2.stop()
