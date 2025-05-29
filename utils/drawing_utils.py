import cv2
import numpy as np
import math
from utils.draw_text_with_background import draw_text_with_background

# Modern color palette
BG_DARK = (30, 30, 30)          # Dark semi-transparent background for text
TEXT_LIGHT = (230, 230, 230)    # Soft off-white text
ACCENT_GREEN = (100, 220, 120)  # Progress bar fill
ACCENT_BLUE = (80, 150, 255)    # Gauge needle and highlights

def display_counter(frame, counter, position=(40, 240), color=TEXT_LIGHT, background_color=BG_DARK):
    """Display the repetition counter with modern style."""
    text = f"Count: {counter}"
    draw_text_with_background(frame, text, position,
                              font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=0.50,
                              text_color=color, bg_color=background_color, thickness=2)

def display_stage(frame, stage, label="Stage", position=(40, 280), color=TEXT_LIGHT, background_color=BG_DARK):
    """Display the current exercise stage with modern style."""
    text = f"{label}: {stage}"
    draw_text_with_background(frame, text, position,
                              font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=0.50,
                              text_color=color, bg_color=background_color, thickness=2)

def draw_progress_bar(frame, exercise, value, position=(40,280), size=(120, 12),
                      color=ACCENT_GREEN, background_color=(50, 50, 50)):
    """Draw a modern progress bar with label and progress text."""
    x, y = position
    width, height = size

    max_values = {"squat": 15, "push_up": 15, "hammer_curl": 15}
    max_value = max_values.get(exercise, 10)

    fill_width = min(int((value / max_value) * width), width)

    # Semi-transparent dark background
    overlay = frame.copy()
    cv2.rectangle(overlay, (x, y), (x + width, y + height), background_color, -1)
    cv2.rectangle(overlay, (x, y), (x + width, y + height), (100, 100, 100), 1)
    cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

    # Fill progress bar
    if fill_width > 0:
        cv2.rectangle(frame, (x, y), (x + fill_width, y + height), color, -1)

    # Progress text centered in the bar
    text = f"{value}/{max_value}"
    (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    text_x = x + (width - tw) // 2
    text_y = y + (height + th) // 2
    cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, TEXT_LIGHT, 1)

    # Label above progress bar with subtle background
    label = f"{exercise.replace('_', ' ').title()} Progress"
    draw_text_with_background(frame, label, (x, y - 18),
                              font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=0.55,
                              text_color=TEXT_LIGHT, bg_color=(50, 0, 0), thickness=1)

def draw_gauge_meter(frame, angle, text, position, radius=40, color=ACCENT_BLUE):
    """Draw a modern gauge meter visualizing joint angle."""
    x, y = position
    start_angle, end_angle = 180, 0

    # Outer circle (light gray)
    cv2.circle(frame, (x, y), radius, (160, 160, 160), 2)

    # Needle angle calculation clamped between start and end
    gauge_angle = max(min(start_angle - angle * (start_angle - end_angle) / 180, start_angle), end_angle)
    rad = math.radians(gauge_angle)
    needle_x = int(x + radius * math.cos(rad))
    needle_y = int(y - radius * math.sin(rad))

    # Needle and center circle
    cv2.line(frame, (x, y), (needle_x, needle_y), color, 3)
    cv2.circle(frame, (x, y), 5, color, -1)

    # Angle text below gauge (darker text for subtlety)
    cv2.putText(frame, f"{int(angle)}°", (x - 18, y + radius + 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (60, 60, 60), 2)

    # Gauge label above the circle with background
    draw_text_with_background(frame, text, (x - radius, y - radius - 20),
                              font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=0.5,
                              text_color=TEXT_LIGHT, bg_color=BG_DARK, thickness=1)
