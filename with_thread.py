import threading
import pygame
from threading import Thread, Lock
import mido
import cv2

# midi filename 생성
midi_filename = []
notes_make_file = [60, 62, 64, 65, 67, 69, 71, 72, 74, 76]
for i, note in enumerate(notes_make_file):    
    midi_filename.append(str(note) + '.mid')
print(midi_filename)

outport = mido.open_output()

def play_mido(midi_filename):
    mid = mido.MidiFile(midi_filename)
    for message in mid.play():
        outport.send(message)

arr1_event = []
# 종료 신호를 전달하기 위한 이벤트 객체
exit_event = threading.Event()

def cam():
    global arr1_event
    cap = cv2.VideoCapture(0)
    cnt = 0
    while not exit_event.is_set():
        # 웹캠에서 프레임 읽기
        ret, frame = cap.read()
        result = cv2.flip(frame, 1)
        
        cv2.imshow("Fingertip Detection division", result)
        arr1_event = [0, 2]
        if 70>cnt > 50:
            arr1_event = [0, 2 ,4]
        elif cnt > 70 :
            arr1_event = [0]

        cnt +=1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit_event.set()  # 종료 신호 설정
            break
    cap.release()
    cv2.destroyAllWindows()

# Thread list 생성
threads_list = []

# 카메라 스레드 추가
cam_thread = threading.Thread(target=cam)
cam_thread.start()
prev_arr1 = []

while not exit_event.is_set():
    while arr1_event != [] and arr1_event != prev_arr1 :
        print(arr1_event)
        prev_arr1 = arr1_event 
        threads_list = []
        # MIDI 파일 재생 스레드 추가
        for i in arr1_event:
            midi_thread = threading.Thread(target=play_mido, args=(midi_filename[i],))
            threads_list.append(midi_thread)

        for t in threads_list:
            t.start()

        for t in threads_list:
            t.join()
    

cam_thread.join()
print('End')

# 종료
pygame.mixer.quit()
pygame.quit()
