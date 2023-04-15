import cv2
import mediapipe as mp

# Initialize Mediapipe Hand Landmark model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)

# Initialize webcam
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    frame= cv2.flip(frame,1) 
    # Convert the frame to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the image using Mediapipe Hand Landmark model
    results = hands.process(image)

    # Extract the landmarks of the hand
    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]

        # Extract the coordinates of the fingertips
        fingertips = []
        for i in range(5):
            landmark = hand_landmarks.landmark[mp_hands.HandLandmark(i*4)]
            x, y = int(landmark.x * image.shape[1]), int(landmark.y * image.shape[0])
            fingertips.append((x, y))

        # Draw circles on the fingertips
        for fingertip in fingertips:
            cv2.circle(frame, fingertip, 5, (255, 0, 0), -1)

    # Show the result
    cv2.imshow("Fingertip Detection", frame)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and destroy all windows
cap.release()
cv2.destroyAllWindows()
