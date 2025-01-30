import cv2

class FallDetection:
    def __init__(self, fall_threshold=0.1, confirm_frames=2, buffer_duration=10):
        self.fall_threshold = fall_threshold
        self.confirm_frames = confirm_frames
        self.buffer_duration = buffer_duration
        self.person_heights = {}
        self.fall_frames = {}
        self.fall_buffer = {}

    def analyze_detection(self, detections, frame_shape):
        
        current_person_ids = []
        rectangles = []  # Liste des rectangles à dessiner
        falls_detected = []

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                class_id = int(detections[0, 0, i, 1])
                if class_id == 15:  # Person class
                    box = detections[0, 0, i, 3:7] * [
                        frame_shape[1], frame_shape[0], frame_shape[1], frame_shape[0]
                    ]
                    (startX, startY, endX, endY) = box.astype("int")
                    rectangles.append((startX, startY, endX, endY, confidence))
                    current_person_ids.append(i)

                    # Calculate height and check for falls
                    height = endY - startY
                    if i in self.person_heights:
                        previous_height = self.person_heights[i]
                        if previous_height > 0:
                            height_change = (previous_height - height) / previous_height
                            if height_change > self.fall_threshold:
                                if self.fall_buffer.get(i, 0) == 0:
                                    self.fall_frames[i] = self.fall_frames.get(i, 0) + 1
                                    if self.fall_frames[i] >= self.confirm_frames:
                                        print(f"Fall detected for person {i}")
                                        falls_detected.append(i)  # Signaler une chute
                                        self.fall_buffer[i] = self.buffer_duration
                            else:
                                self.fall_frames[i] = 0
                    self.person_heights[i] = height

        # Decrement buffers
        for person_id in list(self.fall_buffer.keys()):
            if self.fall_buffer[person_id] > 0:
                self.fall_buffer[person_id] -= 1
            else:
                del self.fall_buffer[person_id]

        return current_person_ids, rectangles, falls_detected