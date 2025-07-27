from sklearn.neighbors import KNeighborsClassifier
import cv2
import numpy as np
import os
import csv
import time
from datetime import datetime
from win32com.client import Dispatch
from database import get_all_students, init_db

def speak(str1):
    speak=Dispatch(("SAPI.SpVoice"))
    speak.Speak(str1)

# Initialize database
init_db()

video=cv2.VideoCapture(0)
facedetect=cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

# Load background image and get screen resolution
bg_img = cv2.imread('bg_test.png')
if bg_img is None:
    print("Error: Could not load bg_test.png")
    exit()

# Get screen resolution
screen_width = 1366  # Standard HD resolution, adjust if needed
screen_height = 745

# Resize background to full screen
bg_img = cv2.resize(bg_img, (screen_width, screen_height))

# Calculate camera frame size and position (left middle)
frame_width = int(844)  # 40% of screen width
frame_height = int(546)  # 4:3 aspect ratio
frame_x = 40  # 40 pixels from left
frame_y = (screen_height - frame_height + 80) // 2  # Centered vertically

# Get student data from database
students, face_encodings = get_all_students()
if len(students) == 0:
    print("No students found in database. Please add students first.")
    exit()

# Setup KNN classifier with dynamic n_neighbors
n_neighbors = min(5, len(students))  # Use at most 5 neighbors, but not more than available samples
if n_neighbors < 1:
    print("Not enough samples in database. Please add more students.")
    exit()

knn = KNeighborsClassifier(n_neighbors=n_neighbors)
knn.fit(face_encodings, range(len(students)))

COL_NAMES = ['NAME', 'STUDENT_CODE', 'BRANCH', 'SESSION', 'TIME']

while True:
    ret,frame = video.read()
    if not ret:
        break
        
    # Create a copy of background for each frame
    final_frame = bg_img.copy()
    
    # Resize camera frame
    frame = cv2.resize(frame, (frame_width, frame_height))
    
    # Process faces
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    
    # Draw rectangles and text on the camera frame
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (50,50,255), 2)
        cv2.rectangle(frame, (x,y-40), (x+w,y), (50,50,255), -1)
        
        # Process face for recognition
        crop_img = frame[y:y+h, x:x+w]
        resized_img = cv2.resize(crop_img, (50,50))
        flattened_img = resized_img.flatten().reshape(1,-1)
        output = knn.predict(flattened_img)
        student = students[output[0]]
        
        cv2.putText(frame, student['name'], (x,y-15), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
        
        # Update attendance record
        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")
        attendance = [student['name'], student['student_code'], student['branch'], student['session'], timestamp]
    
    # Insert camera frame into background
    final_frame[frame_y:frame_y+frame_height, frame_x:frame_x+frame_width] = frame
    
    # Show the combined frame
    cv2.imshow("Attendance System", final_frame)
    
    k=cv2.waitKey(1)
    if k==ord('o'):
        speak("Attendance Taken..")
        time.sleep(5)
        
        # Create Attendance directory if it doesn't exist
        os.makedirs("Attendance", exist_ok=True)
        
        # Check if attendance file exists
        attendance_file = "Attendance/Attendance_" + date + ".csv"
        exist = os.path.exists(attendance_file)
        
        if exist:
            with open(attendance_file, "a") as csvfile:
                writer=csv.writer(csvfile)
                writer.writerow(attendance)
        else:
            with open(attendance_file, "a") as csvfile:
                writer=csv.writer(csvfile)
                writer.writerow(COL_NAMES)
                writer.writerow(attendance)
    if k==ord('q'):
        break
video.release()
cv2.destroyAllWindows()
