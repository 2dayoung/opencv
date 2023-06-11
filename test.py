import threading
import time
import pygame
from threading import Thread, Lock
import mido
import cv2

def long_task():
    for i in range(20):
        time.sleep(0.5)
        print('Working : ' + str(i))


def cam(): 
    cap = cv2.VideoCapture(0)
    while True:
        # 웹캠에서 프레임 읽기
        ret, frame = cap.read()
        result = cv2.flip(frame, 1)


        cv2.imshow("Fingertip Detection division", result)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

threads_list = list()
cam = threading.Thread(target=cam)

threads_list.append(cam)
for i in range(20):
    t = threading.Thread(target=long_task)
    threads_list.append(t)
dd

for t in threads_list:
        t.start()

for t in threads_list:
    t.join()

print('End')

# 종료
pygame.mixer.quit()
pygame.quit()

