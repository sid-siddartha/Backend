import cv2
import numpy as np
import math

def draw_text_with_background(frame, text, position, font=cv2.FONT_HERSHEY_SIMPLEX,
                              font_scale=0.6, text_color=(230, 230, 230),
                              bg_color=(40, 40, 40), thickness=1, padding=5, alpha=0.6):
    """Draw smaller text with a semi-transparent background for readability."""
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    x, y = position
    box_x1 = x
    box_y1 = y - text_height - padding
    box_x2 = x + text_width + 2 * padding
    box_y2 = y + baseline + padding

    overlay = frame.copy()
    cv2.rectangle(overlay, (box_x1, box_y1), (box_x2, box_y2), bg_color, -1)
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    text_position = (x + padding, y)
    cv2.putText(frame, text, text_position, font, font_scale, text_color, thickness, cv2.LINE_AA)

def display_counter(frame, counter, position, color=(230, 230, 230), background_color=(30, 30, 30)):
    """Display the repetition counter in a small box."""
    text = f"Count: {counter}"
    draw_text_with_background(frame, text, position, 
                              font_scale=0.7, text_color=color, bg_color=background_color, thickness=1)

def display_stage(frame, stage, label="Stage", position=(0, 0), color=(230, 230, 230), background_color=(30, 30, 30)):
    """Display the current exercise stage."""
    text = f"{label}: {stage}"
    draw_text_with_background(frame, text, position, 
                              font_scale=0.7, text_color=color, bg_color=background_color, thickness=1)

def draw_progress_bar(frame, exercise, value, position, size=(180, 12), 
                      color=(100, 220, 120), background_color=(30, 30, 30)):
    """Draw a compact progress bar."""
    x, y = position
    width, height = size

    max_values = {"squat": 15, "push_up": 10, "hammer_curl": 12}
    max_value = max_values.get(exercise, 10)

    fill_width = min(int((value / max_value) * width), width)

    # Background with border
    overlay = frame.copy()
    cv2.rectangle(overlay, (x, y), (x + width, y + height), background_color, -1)
    cv2.rectangle(overlay, (x, y), (x + width, y + height), (80, 80, 80), 1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

    # Fill progress bar
    if fill_width > 0:
        cv2.rectangle(frame, (x, y), (x + fill_width, y + height), color, -1)

    # Text inside bar, centered
    text = f"{value}/{max_value}"
    (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    text_x = x + (width - tw) // 2
    text_y = y + height - 2
    cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (240, 240, 240), 1)

    # Label above bar with background
    label = f"{exercise.replace('_', ' ').title()} Progress"
    draw_text_with_background(frame, label, (x, y - 18), 
                              font_scale=0.5, text_color=(230, 230, 230), bg_color=(70, 0, 0), thickness=1)

def draw_gauge_meter(frame, angle, text, position, radius=40, color=(80, 150, 255)):
    """Draw a compact gauge meter."""
    x, y = position
    start_angle, end_angle = 180, 0

    # Outer circle (subtle gray)
    cv2.circle(frame, (x, y), radius, (130, 130, 130), 2)

    # Needle angle clamped between start and end
    gauge_angle = max(min(start_angle - angle * (start_angle - end_angle) / 180, start_angle), end_angle)
    rad = math.radians(gauge_angle)
    needle_x = int(x + radius * math.cos(rad))
    needle_y = int(y - radius * math.sin(rad))

    # Needle and center circle
    cv2.line(frame, (x, y), (needle_x, needle_y), color, 2)
    cv2.circle(frame, (x, y), 4, color, -1)

    # Angle text with shadow for contrast
    cv2.putText(frame, f"{int(angle)}°", (x - 18, y + radius + 20), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (30, 30, 30), 3)
    cv2.putText(frame, f"{int(angle)}°", (x - 18, y + radius + 20), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    # Label above gauge with background
    draw_text_with_background(frame, text, (x - radius, y - radius - 22),
                              font_scale=0.5, text_color=(230, 230, 230), bg_color=(60, 60, 60), thickness=1)

def draw_overlay(frame, right_count, right_stage, left_count, left_stage,
                 exercise, progress_value, right_angle, left_angle):
    h, w = frame.shape[:2]

    overlay_w = w // 3  # reduced width
    overlay_h = h // 3
    overlay_x = w - overlay_w - 20
    overlay_y = 20

    pad_x, pad_y = 12, 18
    current_x = overlay_x + pad_x
    current_y = overlay_y + pad_y

    overlay = frame.copy()
    cv2.rectangle(overlay, (overlay_x, overlay_y),
                  (overlay_x + overlay_w, overlay_y + overlay_h),
                  (20, 20, 20), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

    # Right Counter + Stage
    display_counter(frame, right_count, (current_x, current_y))
    display_stage(frame, right_stage, label="Right Stage", position=(current_x + 130, current_y))
    current_y += 30

    # Left Counter + Stage
    display_counter(frame, left_count, (current_x, current_y))
    display_stage(frame, left_stage, label="Left Stage", position=(current_x + 130, current_y))
    current_y += 40

    # Progress bar
    draw_progress_bar(frame, exercise, progress_value, (current_x, current_y))
    current_y += 40

    # Gauges side-by-side
    right_gauge_pos = (current_x + 40, current_y + 50)
    left_gauge_pos = (current_x + 140, current_y + 50)
    draw_gauge_meter(frame, right_angle, "Right", right_gauge_pos, radius=30)
    draw_gauge_meter(frame, left_angle, "Left", left_gauge_pos, radius=30)
