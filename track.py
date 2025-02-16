## 📋 Updated with Toggle Logging
# Added real-time direction change tracking and Linux compatibility

import cv2
import mediapipe as mp
import pyautogui
import time

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    max_num_faces=1)

## 👁️ Eye Landmark Indices
LEFT_EYE_TOP = 159
LEFT_EYE_BOTTOM = 145
RIGHT_EYE_TOP = 386
RIGHT_EYE_BOTTOM = 374

## ⚙️ Configuration
TOGGLE_THRESHOLD = 0.15  # Start with 0.15, adjust as needed
COOLDOWN = 1.0
MIN_MOVEMENT = 2  # Minimum toggle count before action

# State tracking
last_direction = None
toggle_count = 0
last_toggle_time = 0

def get_eye_state(landmarks, eye_top, eye_bottom):
    top = landmarks[eye_top].y
    bottom = landmarks[eye_bottom].y
    vertical_ratio = (bottom - top) / (bottom + top)
    
    if vertical_ratio > TOGGLE_THRESHOLD:
        return 'up'
    elif vertical_ratio < -TOGGLE_THRESHOLD:
        return 'down'
    return 'neutral'

cap = cv2.VideoCapture(0)

print("👀 Eye Tracking Started! (Press Q to quit)")
print("System: Linux mode with Win key support")

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image)
    
    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark
        
        left_state = get_eye_state(landmarks, LEFT_EYE_TOP, LEFT_EYE_BOTTOM)
        right_state = get_eye_state(landmarks, RIGHT_EYE_TOP, RIGHT_EYE_BOTTOM)
        
        current_state = 'neutral'
        if left_state == right_state and left_state != 'neutral':
            current_state = left_state
        
        # Detect state change
        if current_state != last_direction and current_state != 'neutral':
            print(f"👁️ Toggle detected: {last_direction or 'Start'} → {current_state}")
            toggle_count += 1
        
        # Action trigger logic
        if (current_state != last_direction 
            and current_state != 'neutral'
            and time.time() - last_toggle_time > COOLDOWN):
            
            if last_direction:  # Only trigger after first toggle
                print(f"🚀 Triggering WIN+S (Toggles: {toggle_count})")
                pyautogui.hotkey('win', 's')
                last_toggle_time = time.time()
                toggle_count = 0
                
            last_direction = current_state

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("\n🛑 Eye Tracking Stopped")
