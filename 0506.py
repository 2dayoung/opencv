import cv2
import tkinter as tk
from PIL import Image, ImageTk

class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        
        # 레이블 생성
        self.label = tk.Label(self.window)
        self.label.pack()
        
        # 버튼 생성
        self.button = tk.Button(self.window, text="Show Webcam", command=self.show_webcam)
        self.button.pack()
        
    def show_webcam(self):
        # 웹캠 캡처 객체 생성
        cap = cv2.VideoCapture(0)

        while True:
            # 웹캠에서 이미지 가져오기
            ret, frame = cap.read()

            # 이미지 보여주기
            cv2.imshow('frame', frame)

            # 이미지를 Tkinter에서 사용할 수 있는 형태로 변환
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = image.resize((400, 300), Image.ANTIALIAS)
            image_tk = ImageTk.PhotoImage(image)
            
            # 레이블에 이미지 표시
            self.label.configure(image=image_tk)
            self.label.image = image_tk
            
            # q 키를 누르면 종료
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # 자원 해제
        cap.release()
        cv2.destroyAllWindows()

# 윈도우 생성
window = tk.Tk()

# 애플리케이션 실행
app = App(window, "Tkinter + OpenCV")
window.mainloop()
