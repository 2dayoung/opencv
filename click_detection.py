import cv2
import numpy as np

# Initialize HSV values
h, s, v = 0, 0, 0

# Initialize flag for drawing rectangle
draw_rectangle = False

def get_color(event, x, y, flags, param):
    global h, s, v, draw_rectangle  # Declare the variables as global
    
    if event == cv2.EVENT_LBUTTONDOWN:
        # Retrieve the color at the clicked point in BGR format
        color = frame[y, x]

        # Convert BGR to HSV format
        hsv_color = cv2.cvtColor(np.uint8([[color]]), cv2.COLOR_BGR2HSV)

        # Retrieve the H, S, V values from HSV format
        h, s, v = hsv_color[0][0]

        print(f"Clicked color: BGR({color[2]}, {color[1]}, {color[0]}) | HSV({h}, {s}, {v})")
        
        # Set the flag to True for drawing the rectangle
        draw_rectangle = True

# Open external webcam
cap = cv2.VideoCapture(0)

# Create a window and set the mouse event callback function
cv2.namedWindow('Frame')
cv2.setMouseCallback('Frame', get_color)

while True:
    # Read frames from the webcam
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2.imshow('Frame', frame)

    # Only process the frame if it is properly read
    if ret:
        # Display the frame from the webcam
        

        # Convert the current frame to HSV format
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Create a mask based on the clicked color and its similar range
        lower_hsv = np.array([h - 10, 70, 70])
        upper_hsv = np.array([h + 10, 255, 255])
        mask = cv2.inRange(hsv_frame, lower_hsv, upper_hsv)
        cv2.imshow('mask', mask)
        # kernel = np.ones((5, 5), np.uint8)
        # opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        # closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw rectangles for the detected contours
        
        # Sort contours by area in descending order
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:2]
        
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            cx = x + w // 2
            cy = y + h // 2 
        cv2.rectangle(frame, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), (0, 0, 255), 2)
        
        cv2.imshow('Detected Objects', frame)

       

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
