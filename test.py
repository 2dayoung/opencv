import cv2
import numpy as np
import pygame
from threading import Thread

# Initialize Pygame mixer
pygame.mixer.init()

# Define MIDI filenames
midi_filenames = ['60.mid', '62.mid', '64.mid', '65.mid']

# Define areas
areas = [(50, 50, 150, 150), (200, 50, 300, 150), (350, 50, 450, 150), (500, 50, 600, 150)]



# Define flag for music playing
music_playing = False

# Define callback function for when music is done playing
def music_done_callback():
    global music_playing
    music_playing = False

# Define function to play music in a separate thread
def play_music(midi_filename):
    global music_playing
    music_playing = True
    pygame.mixer.music.load(midi_filename)
    pygame.mixer.music.play()
    while music_playing:
        pygame.time.wait(10)
    music_done_callback()

# Define function to stop music
def stop_music():
    global music_playing
    music_playing = False
    pygame.mixer.music.stop()

# Define function to check if object is in any area
def is_object_in_any_area(location, areas):
    for i in range(len(areas)):
        if is_object_in_area(location, areas[i]):
            return i
    return None

# Define function to check if object is in area
def is_object_in_area(location, area):
    if location[0] > area[0] and location[1] > area[1] and location[0] < area[2] and location[1] < area[3]:
        return True
    else:
        return False

# Open default camera
cap = cv2.VideoCapture(0)

# Set video width and height
cap.set(3, 640)
cap.set(4, 480)

# Define blue color range in HSV
blue_lower = np.array([100, 100, 100])
blue_upper = np.array([130, 255, 255])

while True:
    # Read frame from camera
    ret, frame = cap.read()

    # Convert frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold frame to find blue objects
    mask = cv2.inRange(hsv, blue_lower, blue_upper)
    cv2.imshow('mask', mask)
    # Find contours in the thresholded frame
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw blue circles on objects and check if they are in any area
    object_locations = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 500:
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.circle(frame, (x + w // 2, y + h // 2), 30, (255, 0, 0), 2)
            object_locations.append((x + w // 2, y + h // 2))
    if len(object_locations) > 0:
        event = is_object_in_any_area(object_locations[0], areas)
        if event is not None:
            if not music_playing:
                midi_filename = midi_filenames[event]
                Thread(target=play_music, args=(midi_filename,)).start()
                print('play ',midi_filename)
    color = (255, 0, 0)
    for area in areas:
        x1, y1, x2, y2 = area
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
          

    # Display frame
    cv2.imshow('frame', frame)

    # 'q' 키를 누르면 루프 탈출
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 웹캠 해제 및 모든 윈도우 종료

pygame.midi.quit()
cap.release()
cv2.destroyAllWindows()

