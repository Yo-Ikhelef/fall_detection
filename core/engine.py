import cv2
from core.VideoProcessor import VideoProcessor
from core.MotionDetection import MotionDetection
from core.FallDetection import FallDetection
from core.VideoRecorder import VideoRecorder
from app.services.twilio_service import TwilioService
from decouple import config


class Engine:
    def __init__(self):
        self.video_processor = VideoProcessor()
        self.motion_detection = MotionDetection()
        self.fall_detection = FallDetection()
        self.video_recorder = VideoRecorder()
        self.twilio_service = TwilioService()

    def run(self):
        while True:

            frame = self.video_processor.get_frame()
            if frame is None:
                break

            original_frame = frame.copy()

            # Détection de mouvement
            motion_detected = self.motion_detection.detect_motion(frame)

            # Prétraitement et IA
            blob = self.video_processor.preprocess_frame(frame)
            detections = self.video_processor.forward(blob)

            # Récupérer les rectangles à dessiner
            current_person_ids, rectangles, falls_detected = self.fall_detection.analyze_detection(detections, frame.shape)

            # Dessiner les rectangles sur la frame
            for (startX, startY, endX, endY, confidence) in rectangles:
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                label = f"Person: {confidence:.2f}"
                cv2.putText(frame, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


            # Enregistrement vidéo
            if motion_detected:
                self.video_recorder.start_recording((frame.shape[1], frame.shape[0]))
                self.video_recorder.reset_timeout()

                self.video_recorder.cleanup_old_files()

            if self.video_recorder.recording:
                self.video_recorder.write_frame(original_frame, motion_detected)

            # Envoi SMS en cas de chute
            for person_id in falls_detected:
                self.twilio_service.send_sms(
                    to_phone=config("TWILIO_TO_PHONE"), 
                    message="Alerte : une chute a été détectée !"
                )

            # Affichage
            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # Nettoyage
        self.video_processor.release()
        cv2.destroyAllWindows()

