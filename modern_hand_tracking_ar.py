import cv2
import mediapipe as mp
import numpy as np
from datetime import datetime

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Modern color palette
NEON_BLUE = (255, 120, 0)      # Bright neon blue
NEON_PURPLE = (255, 0, 180)    # Vibrant purple
NEON_CYAN = (255, 255, 0)      # Electric cyan
NEON_PINK = (180, 0, 255)      # Hot pink
WHITE = (255, 255, 255)
DARK_BG = (20, 20, 20)
ACCENT_GREEN = (100, 255, 150)

class ModernUI:
    def __init__(self):
        self.frame_count = 0
        self.gesture_state = "IDLE"
        
    def draw_gradient_circle(self, img, center, radius, color1, color2, thickness=2):
        """Draw a gradient circle with smooth color transition"""
        for i in range(thickness):
            t = i / max(thickness - 1, 1)
            blended = tuple(int(c1 * (1-t) + c2 * t) for c1, c2 in zip(color1, color2))
            cv2.circle(img, center, radius + i, blended, 1)
    
    def draw_glow_effect(self, img, center, radius, color, intensity=0.3):
        """Enhanced glow effect with multiple layers"""
        overlay = np.zeros_like(img, dtype=np.uint8)
        for i in range(5):
            alpha = intensity * (1 - i/5)
            glow_radius = radius + i * 8
            cv2.circle(overlay, center, glow_radius, color, -1)
            cv2.addWeighted(img, 1, overlay, alpha, 0, img)
            overlay.fill(0)
    
    def draw_hexagon(self, img, center, radius, color, thickness=2):
        """Draw a hexagon shape"""
        points = []
        for i in range(6):
            angle = np.deg2rad(60 * i)
            x = int(center[0] + radius * np.cos(angle))
            y = int(center[1] + radius * np.sin(angle))
            points.append([x, y])
        points = np.array(points, np.int32)
        cv2.polylines(img, [points], True, color, thickness)
    
    def draw_particle_ring(self, img, center, radius, color, num_particles=16):
        """Draw animated particle ring"""
        for i in range(num_particles):
            angle = np.deg2rad((i * 360/num_particles) + self.frame_count * 2)
            x = int(center[0] + radius * np.cos(angle))
            y = int(center[1] + radius * np.sin(angle))
            size = 3 + int(2 * np.sin(self.frame_count * 0.1 + i))
            cv2.circle(img, (x, y), size, color, -1)
    
    def draw_tech_lines(self, img, center, radius, color):
        """Draw tech-style radial lines"""
        for i in range(12):
            angle = np.deg2rad(i * 30 + self.frame_count)
            length = 15 if i % 3 == 0 else 10
            x1 = int(center[0] + (radius - length) * np.cos(angle))
            y1 = int(center[1] + (radius - length) * np.sin(angle))
            x2 = int(center[0] + radius * np.cos(angle))
            y2 = int(center[1] + radius * np.sin(angle))
            thickness = 3 if i % 3 == 0 else 2
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)
    
    def draw_hud_corner(self, img, center, offset_x, offset_y, size, color):
        """Draw modern HUD corner brackets"""
        x, y = center[0] + offset_x, center[1] + offset_y
        cv2.line(img, (x, y), (x + size, y), color, 2)
        cv2.line(img, (x, y), (x, y + size), color, 2)
    
    def draw_data_bars(self, img, x, y, values, labels, color):
        """Draw modern data visualization bars"""
        bar_height = 8
        bar_spacing = 25
        
        for i, (value, label) in enumerate(zip(values, labels)):
            y_pos = y + i * bar_spacing
            bar_width = int(150 * (value / 100))
            
            # Background bar
            cv2.rectangle(img, (x, y_pos), (x + 150, y_pos + bar_height), (50, 50, 50), -1)
            # Value bar with gradient
            cv2.rectangle(img, (x, y_pos), (x + bar_width, y_pos + bar_height), color, -1)
            # Label
            cv2.putText(img, label, (x, y_pos - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, WHITE, 1)
            cv2.putText(img, f'{int(value)}%', (x + 155, y_pos + 8), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
    
    def draw_status_panel(self, img, gesture, fps):
        """Draw modern status panel"""
        panel_height = 80
        panel_width = 300
        x, y = 10, 10
        
        # Semi-transparent background
        overlay = img.copy()
        cv2.rectangle(overlay, (x, y), (x + panel_width, y + panel_height), (20, 20, 20), -1)
        cv2.addWeighted(overlay, 0.7, img, 0.3, 0, img)
        
        # Border
        cv2.rectangle(img, (x, y), (x + panel_width, y + panel_height), NEON_BLUE, 2)
        
        # Content
        cv2.putText(img, 'HAND TRACKING AR', (x + 10, y + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, WHITE, 2)
        cv2.putText(img, f'Gesture: {gesture}', (x + 10, y + 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, NEON_CYAN, 1)
        cv2.putText(img, f'FPS: {fps}', (x + 10, y + 65), cv2.FONT_HERSHEY_SIMPLEX, 0.4, ACCENT_GREEN, 1)
        
        # Timestamp
        time_str = datetime.now().strftime('%H:%M:%S')
        cv2.putText(img, time_str, (x + 200, y + 65), cv2.FONT_HERSHEY_SIMPLEX, 0.4, WHITE, 1)
    
    def draw_open_hand_ui(self, img, palm, fingertips, angle):
        """Modern open hand UI"""
        # Main glow effect
        self.draw_glow_effect(img, palm, 100, NEON_BLUE, 0.2)
        
        # Animated hexagons
        for i, radius in enumerate([120, 90, 60]):
            color = NEON_BLUE if i % 2 == 0 else NEON_PURPLE
            self.draw_hexagon(img, palm, radius, color, 2)
        
        # Particle ring
        self.draw_particle_ring(img, palm, 130, NEON_CYAN, 24)
        
        # Tech lines
        self.draw_tech_lines(img, palm, 100, NEON_BLUE)
        
        # Central core
        cv2.circle(img, palm, 25, NEON_PURPLE, -1)
        cv2.circle(img, palm, 25, NEON_PINK, 2)
        cv2.circle(img, palm, 15, NEON_CYAN, 2)
        
        # Fingertip connections with glow
        for i, tip in enumerate(fingertips):
            color = NEON_CYAN if i % 2 == 0 else NEON_PURPLE
            cv2.line(img, palm, tip, color, 2)
            self.draw_glow_effect(img, tip, 8, color, 0.3)
            cv2.circle(img, tip, 8, color, -1)
            cv2.circle(img, tip, 10, WHITE, 1)
        
        # HUD corners
        self.draw_hud_corner(img, palm, -140, -140, 30, NEON_BLUE)
        self.draw_hud_corner(img, palm, 110, -140, 30, NEON_BLUE)
        
        # Angle display
        cv2.putText(img, f'{angle}°', (palm[0] + 50, palm[1] - 50), 
                   cv2.FONT_HERSHEY_DUPLEX, 1.2, NEON_CYAN, 3)
        cv2.putText(img, 'ANGLE', (palm[0] + 50, palm[1] - 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 1)
    
    def draw_pinch_ui(self, img, palm, pinch_value):
        """Modern pinch gesture UI"""
        # Pulsing glow
        pulse = int(20 + 10 * np.sin(self.frame_count * 0.2))
        self.draw_glow_effect(img, palm, 50 + pulse, NEON_PINK, 0.3)
        
        # Animated circles
        for i in range(3):
            radius = 60 + i * 20
            alpha = (self.frame_count + i * 40) % 360
            cv2.ellipse(img, palm, (radius, radius), 0, alpha, alpha + 120, NEON_PINK, 3)
        
        # Central indicator
        cv2.circle(img, palm, 40, NEON_PURPLE, -1)
        cv2.circle(img, palm, 40, NEON_PINK, 3)
        
        # Pinch value arc
        arc_radius = 80
        arc_angle = int(pinch_value * 3.6)
        cv2.ellipse(img, palm, (arc_radius, arc_radius), -90, 0, arc_angle, ACCENT_GREEN, 5)
        
        # Value display
        cv2.putText(img, f'{pinch_value}%', (palm[0] - 30, palm[1] + 10), 
                   cv2.FONT_HERSHEY_DUPLEX, 1, WHITE, 2)
        cv2.putText(img, 'PINCH', (palm[0] - 35, palm[1] - 100), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, NEON_PINK, 2)
    
    def draw_fist_ui(self, img, palm):
        """Modern fist gesture UI"""
        # Rotating hexagon
        angle_offset = self.frame_count * 3
        overlay = img.copy()
        
        # Multiple rotating hexagons
        for i, radius in enumerate([100, 70, 40]):
            color = NEON_BLUE if i == 0 else NEON_PURPLE if i == 1 else NEON_CYAN
            points = []
            for j in range(6):
                angle = np.deg2rad(60 * j + angle_offset * (1 if i % 2 == 0 else -1))
                x = int(palm[0] + radius * np.cos(angle))
                y = int(palm[1] + radius * np.sin(angle))
                points.append([x, y])
            points = np.array(points, np.int32)
            cv2.polylines(img, [points], True, color, 3)
        
        # Central pulse
        pulse_size = int(20 + 10 * np.sin(self.frame_count * 0.15))
        cv2.circle(img, palm, pulse_size, NEON_CYAN, -1)
        cv2.circle(img, palm, pulse_size + 5, NEON_BLUE, 2)
        
        # Status text
        cv2.putText(img, 'LOCKED', (palm[0] - 50, palm[1] - 120), 
                   cv2.FONT_HERSHEY_DUPLEX, 1, NEON_BLUE, 3)

# Initialize
ui = ModernUI()
cap = cv2.VideoCapture(0)
prev_time = 0

print("Starting Modern Hand Tracking AR UI...")
print("Gestures:")
print("  - Open Hand: Full AR interface")
print("  - Pinch: Interactive control")
print("  - Fist: Locked state")
print("Press ESC to exit")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    
    # Calculate FPS
    current_time = cv2.getTickCount()
    fps = int(cv2.getTickFrequency() / (current_time - prev_time)) if prev_time > 0 else 0
    prev_time = current_time
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            h, w, _ = frame.shape
            lm = [(int(l.x * w), int(l.y * h)) for l in hand_landmarks.landmark]
            
            # Draw minimal hand skeleton
            connections = mp_hands.HAND_CONNECTIONS
            for connection in connections:
                start_idx, end_idx = connection
                cv2.line(frame, lm[start_idx], lm[end_idx], (100, 100, 100), 1)
            
            palm = lm[9]
            fingertips = [lm[i] for i in [4, 8, 12, 16, 20]]
            
            # Calculate metrics
            dists = [np.linalg.norm(np.array(tip) - np.array(palm)) for tip in fingertips]
            avg_dist = np.mean(dists)
            pinch_dist = np.linalg.norm(np.array(lm[4]) - np.array(lm[8]))
            pinch_value = int(100 - min(pinch_dist, 100))
            
            # Gesture detection and rendering
            if avg_dist > 70:
                ui.gesture_state = "OPEN HAND"
                v1 = np.array(lm[4]) - np.array(palm)
                v2 = np.array(lm[8]) - np.array(palm)
                try:
                    angle = int(np.degrees(np.arccos(
                        np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-6)
                    )))
                except:
                    angle = 0
                ui.draw_open_hand_ui(frame, palm, fingertips, angle)
                
            elif pinch_value > 40:
                ui.gesture_state = "PINCH"
                ui.draw_pinch_ui(frame, palm, pinch_value)
                
            else:
                ui.gesture_state = "FIST"
                ui.draw_fist_ui(frame, palm)
    else:
        ui.gesture_state = "NO HAND"
    
    # Draw status panel
    ui.draw_status_panel(frame, ui.gesture_state, fps)
    
    # Increment frame counter for animations
    ui.frame_count += 1
    
    cv2.imshow('Modern Hand Tracking AR', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
print("Application closed.")
