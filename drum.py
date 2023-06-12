import cv2
import simpleaudio as sa
import pygame.midi
import time
import mido
import numpy as np
import simpleaudio as sa
from tkinter import *

mouse_click_count = 0
roi_points = []
mouse_drag_started = False
rectangles = []

def play_drum_sound(sound_file):
    wave_obj = sa.WaveObject.from_wave_file(sound_file)
    play_obj = wave_obj.play()
    play_obj.wait_done()

def mouse_callback(event, x, y, flags, param):
    global mouse_drag_started, roi_points, mouse_click_count, rectangles

    if event == cv2.EVENT_LBUTTONDOWN:
        if mouse_click_count < 2:
            # 좌표 출력
            print(f"Clicked: ({x}, {y})")
            roi_points.append((x, y))
            mouse_click_count += 1

        if mouse_click_count == 2:
            mouse_click_count = 0
            mouse_drag_started = True
            roi_points = roi_points[-2:]  

            if len(rectangles) < 4:
                x1, y1 = roi_points[0]
                x2, y2 = roi_points[1]
                rectangles.append((x1, y1, x2, y2))
            else:
                mouse_drag_started = False

cap = cv2.VideoCapture(0)
cv2.namedWindow('img')

# 드럼 소리를 재생할 오디오 파일 경로
drum_sound1 = sa.WaveObject.from_wave_file('drum/hihat.wav')
drum_sound2 = sa.WaveObject.from_wave_file('drum/snare.wav')
drum_sound3 = sa.WaveObject.from_wave_file('drum/mid_tom.wav')
drum_sound4 = sa.WaveObject.from_wave_file('drum/kick.wav')

event = None
prev_event = 0

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    if not ret:
        break

    # 이미지 크기 조정
    frame = cv2.resize(frame, (800, 600))
    
    # 이미지를 BGR에서 HSV로 변환
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    img = frame.copy()
    cv2.setMouseCallback('img', mouse_callback)

    if mouse_drag_started:
        x1, y1 = roi_points[0]
        x2, y2 = roi_points[1]

        color = [(255, 165, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0)][len(rectangles)]

        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

    # 앞서 그린 사각형들이 안 없어지도록 
    for i, rect in enumerate(rectangles):
        x1, y1, x2, y2 = rect
        color = [(0, 165, 255), (0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 0, 0)][i]


        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

    cv2.imshow('img', img)

    lower_blue = (90, 100, 100)
    upper_blue = (120, 255, 255)
    # HSV 이미지에서 색상 범위에 해당하는 영역을 이진화합니다.
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # 잡음 제거를 위한 모폴로지 연산
    kernel = np.ones((5,5),np.uint8)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    cv2.imshow("closing ",closing )
    
    # 객체 검출
    contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 두 개의 가장 큰 객체만 추출
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:2]

    if contours and len(rectangles) > 3:
        # 객체 위치 추출
        event = [-1, -1]  # 두 개의 객체에 대한 event 초기화
        for i, c in enumerate(contours):
            x, y, w, h = cv2.boundingRect(c)
            cx = x + w // 2
            cy = y + h // 2
     
            # 원 중심 좌표를 사용하여 소리 재생
            if rectangles[0][0] < cx < rectangles[0][2] and rectangles[0][1] < cy < rectangles[0][3]:
                event[i] = 1
            elif rectangles[1][0] < cx < rectangles[1][2] and rectangles[1][1] < cy < rectangles[1][3]:
                event[i] = 2
            elif rectangles[2][0] < cx < rectangles[2][2] and rectangles[2][1] < cy < rectangles[2][3]:
                event[i] = 3
            elif rectangles[3][0] < cx < rectangles[3][2] and rectangles[3][1] < cy < rectangles[3][3]:
                event[i] = 4
                

            cv2.rectangle(img, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), (0, 0, 255), 2)
            
        # 두 개의 event 값을 독립적으로 처리
        if event[0] != -1:
            if event[0] == prev_event[0]:
                pass
            elif event[0] == 1:
                drum_sound1.play()
                print("play", event[0])
            elif event[0] == 2:
                drum_sound2.play()
                print("play", event[0])
            elif event[0] == 3:
                drum_sound3.play()
                print("play", event[0])
            elif event[0] == 4:
                drum_sound4.play()
                print("play", event[0])

        if event[1] != -1:
            if event[1] == prev_event[1]:
                pass
            elif event[1] == 1:
                drum_sound1.play()
                print("play", event[1])
            elif event[1] == 2:
                drum_sound2.play()
                print("play", event[1])
            elif event[1] == 3:
                drum_sound3.play()
                print("play", event[1])
            elif event[1] == 4:
                drum_sound4.play()
                print("play", event[1])

        prev_event = event
        print(event)
    
    # 결과 출력
    cv2.imshow('img', img)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()