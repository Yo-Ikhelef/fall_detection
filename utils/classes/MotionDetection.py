import cv2

class MotionDetection:
    def __init__(self, motion_threshold=5000):
        self.previous_frame = None
        self.motion_threshold = motion_threshold

    def detect_motion(self, frame):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

        if self.previous_frame is None:
            self.previous_frame = gray_frame
            return False

        frame_diff = cv2.absdiff(self.previous_frame, gray_frame)
        _, thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)
        motion_pixels = cv2.countNonZero(thresh)

        self.previous_frame = gray_frame

        return motion_pixels > self.motion_threshold
