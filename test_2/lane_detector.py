import cv2
import numpy as np

class LaneDetector:

    @staticmethod
    def detect_lanes(image):
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Step 2) Gray Scale
        gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        gray_img = cv2.dilate(gray_img, kernel=np.ones((5, 5), np.uint8))
        # Step 3) Canny
        canny = cv2.Canny(gray_img, 100, 200)
        # Step 4) define ROI Vertices
        roi_vertices = [(200, 200), (200, 800), (800, 200), (800, 800)]
        roi_image = LaneDetector.roi(canny, np.array([roi_vertices], np.int32))
        lines = cv2.HoughLinesP(roi_image, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)
        final_img = LaneDetector.draw_lines(img, lines)
        cv2.imshow("result", roi_image)
        cv2.waitKey(1)

    @staticmethod
    def roi(image, vertices):
        mask = np.zeros_like(image)
        mask_color = 255
        cv2.fillPoly(mask, vertices, mask_color)
        masked_img = cv2.bitwise_and(image, mask)
        return masked_img
    
    @staticmethod
    def draw_lines(image, hough_lines):
        try:
            for line in hough_lines:
                x1, y1, x2, y2 = line[0]
                # Calculate midpoint of the line segment
                mid_x = (x1 + x2) // 2
                mid_y = (y1 + y2) // 2
                # Draw a circle (dot) at the midpoint
                cv2.circle(image, (mid_x, mid_y), 2, (0, 255, 0), -1)  # -1 for filled circle
        except Exception:
            return image

        return image