import cv2
from pose_estimation.angle_calculation import calculate_angle

class Squat:
    def __init__(self):
        self.counter = 0
        self.stage = None

    def calculate_angle(self, point1, point2, point3):
        return calculate_angle(point1, point2, point3)  # Calculates angle at point2

    def track_squat(self, landmarks, frame):
        # Extract coordinates
        hip_left = [int(landmarks[23].x * frame.shape[1]), int(landmarks[23].y * frame.shape[0])]
        knee_left = [int(landmarks[25].x * frame.shape[1]), int(landmarks[25].y * frame.shape[0])]
        ankle_left = [int(landmarks[27].x * frame.shape[1]), int(landmarks[27].y * frame.shape[0])]

        hip_right = [int(landmarks[24].x * frame.shape[1]), int(landmarks[24].y * frame.shape[0])]
        knee_right = [int(landmarks[26].x * frame.shape[1]), int(landmarks[26].y * frame.shape[0])]
        ankle_right = [int(landmarks[28].x * frame.shape[1]), int(landmarks[28].y * frame.shape[0])]

        # Calculate angles at the knees
        angle_left = self.calculate_angle(hip_left, knee_left, ankle_left)
        angle_right = self.calculate_angle(hip_right, knee_right, ankle_right)

        # Draw lines for visualization
        self.draw_line_with_style(frame, hip_left, knee_left, (178, 102, 255), 2)
        self.draw_line_with_style(frame, knee_left, ankle_left, (178, 102, 255), 2)
        self.draw_circle(frame, hip_left, (178, 102, 255), 8)
        self.draw_circle(frame, knee_left, (178, 102, 255), 8)
        self.draw_circle(frame, ankle_left, (178, 102, 255), 8)

        self.draw_line_with_style(frame, hip_right, knee_right, (51, 153, 255), 2)
        self.draw_line_with_style(frame, knee_right, ankle_right, (51, 153, 255), 2)
        self.draw_circle(frame, hip_right, (51, 153, 255), 8)
        self.draw_circle(frame, knee_right, (51, 153, 255), 8)
        self.draw_circle(frame, ankle_right, (51, 153, 255), 8)

        # Display angles
        cv2.putText(frame, f'Left: {int(angle_left)}', (knee_left[0] + 10, knee_left[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.putText(frame, f'Right: {int(angle_right)}', (knee_right[0] + 10, knee_right[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # Use the average of both knee angles
        avg_knee_angle = (angle_left + angle_right) / 2

        # Rep counting logic based on knee angle
        if avg_knee_angle > 160:
            if self.stage == 'Ascent':
                self.counter += 1
                self.stage = 'Starting Position'
            else:
                self.stage = 'Starting Position'
        elif avg_knee_angle < 110:
            if self.stage == 'Starting Position':
                self.stage = 'Descent'
            elif self.stage == 'Descent':
                self.stage = 'Ascent'

        # Optional debug log
        print(f"Avg Angle: {avg_knee_angle}, Stage: {self.stage}, Count: {self.counter}")

        return self.counter, avg_knee_angle, self.stage

    def draw_line_with_style(self, frame, start_point, end_point, color, thickness):
        cv2.line(frame, start_point, end_point, color, thickness, lineType=cv2.LINE_AA)

    def draw_circle(self, frame, center, color, radius):
        cv2.circle(frame, center, radius, color, -1)  # Filled circle
