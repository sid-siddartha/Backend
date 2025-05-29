import cv2
import numpy as np

def draw_text_with_background(frame, text, position, font=cv2.FONT_HERSHEY_SIMPLEX,
                              font_scale=0.8, text_color=(255, 255, 255), 
                              bg_color=(50, 50, 50), thickness=2, padding=8, alpha=0.7):
    # Get size of the text box
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    x, y = position
    box_x1 = x
    box_y1 = y - text_height - padding
    box_x2 = x + text_width + 2 * padding
    box_y2 = y + baseline + padding

    # Semi-transparent background
    overlay = frame.copy()
    cv2.rectangle(overlay, (box_x1, box_y1), (box_x2, box_y2), bg_color, -1)
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    # Draw text with padding
    text_position = (x + padding, y)
    cv2.putText(frame, text, text_position, font, font_scale, text_color, thickness, cv2.LINE_AA)
