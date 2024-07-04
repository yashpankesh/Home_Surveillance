import cv2
import time
from datetime import datetime

# Replace the camera initialization with the URL of the mobile device stream
url = 'http://192.168.1.7:8080/video'  # Replace with the actual URL
cap = cv2.VideoCapture(url)
time.sleep(2)  # Warm up the camera

# Initialize variables
last_frame = None
alert_issued = False

def detect_motion(frame1, frame2):
    # Convert frames to grayscale
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to the frames
    gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)
    gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)
    
    # Compute the absolute difference between the two frames
    frame_delta = cv2.absdiff(gray1, gray2)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    
    # Find contours on the thresholded image
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Check if any contour area is significant
    motion_detected = any(cv2.contourArea(c) > 500 for c in contours)
    
    return motion_detected

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    if last_frame is None:
        last_frame = frame
        continue
    
    if detect_motion(last_frame, frame) and not alert_issued:
        alert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Motion detected at {alert_time}! Alert issued.")
        alert_issued = True
        alert_start_time = time.time()
    
    if alert_issued and time.time() - alert_start_time > 5:
        print("Resetting alert.")
        alert_issued = False
    
    # Show the current frame
    cv2.imshow('Frame', frame)
    
    # Update the last frame
    last_frame = frame
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()