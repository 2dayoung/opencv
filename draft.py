#파란 원 영역에 들어오면 점수 + 트랙바 

import cv2
import numpy as np
import simpleaudio as sa

# 특정 영역과 실행할 wav 파일을 딕셔너리로 저장

do = sa.WaveObject.from_wave_file("sounds/1.wav")
re = sa.WaveObject.from_wave_file("sounds/2.wav")
mi = sa.WaveObject.from_wave_file("sounds/3.wav")
fa = sa.WaveObject.from_wave_file("sounds/4.wav")
# wav 파일 로드


# 트랙바를 위한 콜백 함수
def nothing(x):
    pass

# 웹캠에서 프레임을 캡처합니다.
cap = cv2.VideoCapture(0)

# 노란색 범위 설정 (HSV)
lower = (17, 94, 94)
upper = (32, 255, 255)

# 웹캠 캡처 생성
cap = cv2.VideoCapture(0)

#in인지 상태 저장 변수
do_in=False
re_in=False
mi_in=False
fa_in=False

while True:
    # 현재 프레임 캡처
    ret, frame = cap.read()

    # 프레임이 캡처되지 않았으면 종료
    if not ret:
        break

    # 이미지 크기 조정
    frame = cv2.resize(frame, (640, 480))

    #화면 반전
    result= cv2.flip(frame,1) 

    # 이미지를 BGR에서 HSV로 변환
    hsv = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)

    # HSV 이미지에서 색상 범위에 해당하는 영역을 이진화합니다.
    mask = cv2.inRange(hsv, lower, upper)
    cv2.imshow("mask",mask)

    # 잡음 제거를 위한 모폴로지 연산
    kernel = np.ones((5,5),np.uint8)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

    # 객체 검출
    contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 두 개의 가장 큰 객체만 추출
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:2]
    
    # 객체 위치 추출
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)

        #x와 y를 객체 중심점으로 바꾸기 
        x= x + w//2
        y= y + h//2
        #print("x , y =",x,y)
        if x > 80 and x <190 and y > 300 and y < 360:
            cv2.putText(result, "Do", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            

        elif x > 190 and x < 300 and y > 300 and y < 360:
            cv2.putText(result, "Re", (170, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

           
   
        elif x > 300 and x <410 and y > 300 and y < 360:
            cv2.putText(result, "Mi", (330, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

           
       
        elif x > 410 and x < 520 and y > 300 and y < 360:
            cv2.putText(result, "Fa", (490, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        elif x > 520 and x < 620 and y > 300 and y < 360:
            cv2.putText(result, "sol", (490, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

  
        cv2.rectangle(result, (x-w//2, y-h//2), (x+w//2, y+h//2), (0, 0, 255), 2)

   
    if do_in and not re_in and not mi_in and not fa_in:
    
        do.play()
        do_in = False  
            
    if not do_in and re_in and not mi_in and not fa_in:

        re.play()
        re_in=False

    
    if not do_in and not re_in and mi_in and not fa_in:

        mi.play()  
        mi_in=False
        
    if not do_in and not re_in and not mi_in and  fa_in:

        fa.play()
        fa_in=False


    # 영역 표시 
    cv2.rectangle(result, (80, 300),(180, 360),(0,0,255),2),  #도 
    cv2.rectangle(result,(190, 300),(290, 360),(54,148,255),2)  #레
    cv2.rectangle(result,(300, 300),(400, 360),(0,228,255),2)  #미
    cv2.rectangle(result,(410, 300),(510, 360),(22,219,29),2)  #파
    cv2.rectangle(result,(520, 300),(620, 360),(22,2,29),2)  #파


    # 이미지 출력
    cv2.imshow("Webcam", result)

    # q 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 자원 해제
cap.release()
cv2.destroyAllWindows()
