import cv2
import mediapipe as mp
import simpleaudio as sa
import pygame.midi
import time
import mido
import numpy as np
import simpleaudio as sa
from tkinter import *

def play_drum(sound_file):
    wave_obj = sa.WaveObject.from_wave_file(sound_file)
    play_obj = wave_obj.play()
    play_obj.wait_done()

# 웹캠 초기화
cap = cv2.VideoCapture(1)

# 드럼 소리를 재생할 오디오 파일 경로
drum_sound1 = sa.WaveObject.from_wave_file('kick.wav')
drum_sound2 = sa.WaveObject.from_wave_file('snare.wav')
drum_sound3 = sa.WaveObject.from_wave_file('hihat.wav')

# 직사각형 영역 정보
rectangle1 = [(80, 250), (180, 400)]  # 좌상단, 우하단 좌표
rectangle2 = [(280, 250), (380, 400)]
rectangle3 = [(480, 250), (580, 400)]

event = None
prev_event = 0
while True:
    # 웹캠에서 프레임 읽기& 좌우반전 &크기
    ret, frame = cap.read()
    frame= cv2.flip(frame,1)

    # 이미지 크기 조정
    frame = cv2.resize(frame, (640, 480))
    
    # 이미지를 BGR에서 HSV로 변환
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 직사각형 그리기
    cv2.rectangle(frame, rectangle1[0], rectangle1[1], (0, 0, 255), 2)
    cv2.rectangle(frame, rectangle2[0], rectangle2[1], (0, 255, 0), 2)
    cv2.rectangle(frame, rectangle3[0], rectangle3[1], (255, 0, 0), 2)
    lower_blue = (90, 150, 150)
    upper_blue = (120, 255, 255)
    # HSV 이미지에서 색상 범위에 해당하는 영역을 이진화합니다.
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    #cv2.imshow("mask",mask)
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

    if contours:
        # 객체 위치 추출
        event = [-1, -1]  # 두 개의 객체에 대한 event 초기화
        for i, c in enumerate(contours):
            x, y, w, h = cv2.boundingRect(c)
            cx = x + w // 2
            cy = y + h // 2

            # 원 중심 좌표를 사용하여 소리 재생
            if rectangle1[0][0] < cx < rectangle1[1][0] and rectangle1[0][1] < cy < rectangle1[1][1]:
                event[i] = 1
            elif rectangle2[0][0] < cx < rectangle2[1][0] and rectangle2[0][1] < cy < rectangle2[1][1]:
                event[i] = 2
            elif rectangle3[0][0] < cx < rectangle3[1][0] and rectangle3[0][1] < cy < rectangle3[1][1]:
                event[i] = 3

            cv2.rectangle(frame, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), (0, 0, 255), 2)

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

        prev_event = event
        print(event)


    #결과 출력
    cv2.imshow('Drum Detection', frame)

    #'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#웹캠 해제 및 창 닫기
cap.release()
cv2.destroyAllWindows()
