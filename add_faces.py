import cv2
import numpy as np
from database import init_db, add_student
import sqlite3

# Get student details from temp file
try:
    with open('temp_student_details.txt', 'r') as f:
        name = f.readline().strip()
        student_code = f.readline().strip()
        branch = f.readline().strip()
        session = f.readline().strip()
except FileNotFoundError:
    print("Error: Student details not found")
    exit(1)

# Initialize database first
try:
    init_db()
except sqlite3.Error as e:
    print(f"Database error: {e}")
    exit(1)

# Get screen resolution
screen_width = 1366  # Standard HD resolution, adjust if needed
screen_height = 745

# Load and resize background image
bg_img = cv2.imread('bg_add_faces.png')
if bg_img is None:
    print("Error: Could not load bg_add_faces.png")
    exit()
bg_img = cv2.resize(bg_img, (screen_width, screen_height))

# Calculate camera frame size and position
frame_width = int(844)  # 40% of screen width
frame_height = int(546)  # 4:3 aspect ratio
frame_x = 40  # 40 pixels from left
frame_y = (screen_height - frame_height) // 2  # Centered vertically

#capturing video
video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
faces_data = []

i = 0

#starting camera
while True:
    ret,frame=video.read()
    if not ret:
        break
        
    # Create a copy of background for each frame
    final_frame = bg_img.copy()
    
    # Resize camera frame
    frame = cv2.resize(frame, (frame_width, frame_height))
    
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces=facedetect.detectMultiScale(gray, 1.3 ,5)
    for (x,y,w,h) in faces:
        crop_img = frame[y:y+h, x:x+w]
        resized_img = cv2.resize(crop_img, (50,50))
        if len(faces_data)<=100 and i%10==0:
            faces_data.append(resized_img)
        i=i+1
        
        # Draw on frame
        cv2.rectangle(frame, (x,y), (x+w, y+h), (50,50,255), 2)
        cv2.putText(frame, f"Images Captured: {len(faces_data)}", (30,30), 
                    cv2.FONT_HERSHEY_COMPLEX, 1, (50,50,255), 2)
        
    # Insert camera frame into background
    final_frame[frame_y:frame_y+frame_height, frame_x:frame_x+frame_width] = frame
    
    # Add text instructions to background
    cv2.putText(final_frame, "Press 'q' to quit", (frame_x + frame_width + 30, frame_y + 30), 
                cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
    cv2.putText(final_frame, f"Capturing: {name}", (frame_x + frame_width + 30, frame_y + 70), 
                cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
    cv2.putText(final_frame, f"Progress: {len(faces_data)}/100", (frame_x + frame_width + 30, frame_y + 110), 
                cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
    
    # Show the combined frame
    cv2.imshow("Add Face - Attendance System", final_frame)
    
    k=cv2.waitKey(1)
    if k==ord('q') or len(faces_data)==100:
        break

video.release()
cv2.destroyAllWindows()

faces_data = np.asarray(faces_data)
faces_data = faces_data.reshape(100, -1)  # Will now be 100 x 7500 (50x50x3)

# Save to database
if len(faces_data) == 100:
    face_encoding = faces_data.mean(axis=0)  # Average face encoding
    try:
        add_student(student_code, name, branch, session, face_encoding)
        print("Student data saved successfully!")
    except sqlite3.Error as e:
        print(f"Database error: {e}")

cv2.destroyAllWindows()