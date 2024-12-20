import cv2
from .Contours import Contours

class UpdateFrame: 
    def __init__(self, prev_frame=None): 
        self.prev_frame = prev_frame
    
    def update_frame(self, frame): 
        instance_contours = Contours(frame)
        
        if self.prev_frame is None: 
            self.prev_frame = instance_contours.edges
            return instance_contours.edges
        diff = cv2.absdiff(instance_contours.edges, self.prev_frame)
        _, thresh = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)
        self.prev_frame = instance_contours.edges
        return thresh