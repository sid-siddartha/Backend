# feedback/indicators.py
from utils.drawing_utils import draw_gauge_meter, draw_progress_bar, display_stage, display_counter

# Colors (modern palette)
BG_DARK = (30, 30, 30)  # Dark background for text boxes
TEXT_LIGHT = (230, 230, 230)
ACCENT_GREEN = (100, 220, 120)
ACCENT_BLUE = (80, 150, 255)
ACCENT_YELLOW = (255, 210, 70)

# Positions relative to frame size (top-right overlay area)
def get_overlay_positions(frame):
    h, w = frame.shape[:2]
    overlay_x = w - (w // 3)   # start 25% from right with margin
    base_y = 40
    spacing_y = 35
    return overlay_x, base_y, spacing_y

def draw_squat_indicators(frame, counter, angle, stage):
    overlay_x, base_y, spacing_y = get_overlay_positions(frame)

    # Counter
    display_counter(frame, counter, position=(overlay_x, base_y), color=TEXT_LIGHT, background_color=BG_DARK)

    # Stage
    display_stage(frame, stage, "Stage", position=(overlay_x, base_y + spacing_y), color=TEXT_LIGHT, background_color=BG_DARK)

    # Progress bar below stage
    draw_progress_bar(frame, exercise="squat", value=counter, position=(overlay_x, base_y + 2 * spacing_y), 
                      size=(180, 15), color=ACCENT_GREEN, background_color=(50, 50, 50))

    # Gauge meter below progress bar, aligned center of overlay box width
    gauge_pos = (overlay_x + 50, base_y + 2 * spacing_y + 50)
    draw_gauge_meter(frame, angle=angle, text="Squat Angle", position=gauge_pos, radius=40, color=ACCENT_BLUE)


def draw_pushup_indicators(frame, counter, angle, stage):
    overlay_x, base_y, spacing_y = get_overlay_positions(frame)

    display_counter(frame, counter, position=(overlay_x, base_y), color=TEXT_LIGHT, background_color=BG_DARK)

    display_stage(frame, stage, "Stage", position=(overlay_x, base_y + spacing_y), color=TEXT_LIGHT, background_color=BG_DARK)

    draw_progress_bar(frame, exercise="push_up", value=counter, position=(overlay_x, base_y + 2 * spacing_y),
                      size=(180, 15), color=ACCENT_GREEN, background_color=(50, 50, 50))

    gauge_pos = (overlay_x + 90, base_y + 2 * spacing_y + 90)
    draw_gauge_meter(frame, angle=angle, text="Push-up Angle", position=gauge_pos, radius=20, color=ACCENT_BLUE)


def draw_hammercurl_indicators(frame, counter_right, angle_right, counter_left, angle_left, stage_right, stage_left):
    overlay_x, base_y, spacing_y = get_overlay_positions(frame)

    # Right arm indicators
    display_counter(frame, counter_right, position=(overlay_x, base_y), color=TEXT_LIGHT, background_color=BG_DARK)
    display_stage(frame, stage_right, "Right Stage", position=(overlay_x, base_y + spacing_y), color=TEXT_LIGHT, background_color=BG_DARK)

    # Left arm indicators below right arm stage
    left_stage_y = base_y + 2 * spacing_y
    display_counter(frame, counter_left, position=(overlay_x, left_stage_y), color=TEXT_LIGHT, background_color=BG_DARK)
    display_stage(frame, stage_left, "Left Stage", position=(overlay_x, left_stage_y + spacing_y), color=TEXT_LIGHT, background_color=BG_DARK)

    # Progress bar centered between counters/stages
    progress_y = base_y + 4 * spacing_y + 10
    avg_counter = (counter_right + counter_left) / 2
    draw_progress_bar(frame, exercise="hammer_curl", value=avg_counter, position=(overlay_x, progress_y), 
                      size=(180, 15), color=ACCENT_GREEN, background_color=(50, 50, 50))

    # Gauge meters for angles - placed side by side below progress bar
    gauge_y = progress_y + 45
    right_gauge_pos = (overlay_x + 50, gauge_y)
    left_gauge_pos = (overlay_x + 130, gauge_y)

    draw_gauge_meter(frame, angle=angle_right, text="Right Angle", position=right_gauge_pos, radius=30, color=ACCENT_BLUE)
    draw_gauge_meter(frame, angle=angle_left, text="Left Angle", position=left_gauge_pos, radius=30, color=ACCENT_BLUE)
