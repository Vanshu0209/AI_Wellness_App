import cv2
import numpy as np

class BodyAnalyzerCV:
    def __init__(self):
        pass

    def process_image(self, image_path):
        img = cv2.imread(image_path)
        if img is None:
            return None, "Unknown", 0.0

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        shape = "Rectangle"
        ratio = 1.0
        
        if contours:
            largest = max(contours, key=cv2.contourArea)
            x, y, cw, ch = cv2.boundingRect(largest)
            cv2.rectangle(img, (x, y), (x + cw, y + ch), (0, 255, 0), 2)
            ratio = ch / float(cw) if cw > 0 else 1.0
            
            if ratio > 2.2:
                shape = "Rectangle"
            elif ratio > 1.8:
                shape = "Inverted Triangle"
            else:
                shape = "Hourglass"
                
        return img, shape, ratio
