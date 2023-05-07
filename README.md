### 소리내는 방법

1. pygame 이용 
(이건 키보드 이용할 때만 필요할 수도)
2. simpleaudio 이용

### 소리파일 
1. 비프음
2. wav파일
- 무료다운 사이트 찾아야함
   - https://samplefocus.com/collections/keys-notes
- https://github.com/ky0422/keyboard/tree/main/public/resources/notes

- 직접 녹음

3. MIDI를 사용해서 추출하기       
 - - -      
 
종합설계
========

 영역에 들어오면 소리
 
**idea**
 - 카메라를 위에하나 앞쪽에 하나 둬서 같은 포인트를 찾아서 위에 카메라는 위치만 인식하고 아래 카메라는 위아래 높이를 인식해서 press인지 확인
 - 
 
 - 원 두개를 검출해서 왼쪽 영역에 오면 스코어 올라감 + 트랙바 
## 2023-04-09
- 키보드 1234 누르면 도레미파 소리 나옴 pygame 사용 
- 비프음출력 

>**할것** 
* 영역을 4개로 나눠서 나눈 영역에 들어오면 wav로 소리 나게 합치기 
* 건반 영역 검출 
* 카메라를 어디에 둘지 
* 손가락 포기할것인지 고민
* 밝기나 그런것들이 달라질텐데 어떻게 자동 보정할지 고민

## 2023-04-10
 **목표** 영역 4개로 나눠서 나눈 영역에 들어오면 어떤 영역에 들어왔는지 구분하기 

- 파란 원을 잘 못잡아냄 -> 보정(잡음제거)를 좀 하고 더 작은것도 인식되도록 하여 더 잘 인식되게한다. 
- 파란 원 잡는것 더 잘 되게 바꿈 ( 두개만 잡도록)
- 영역 4개나눠서 어떤 영역에 들어왔는지 구분하게됨 (도레미파)
- 소리 나게함( 문제있음: 영역에 들어오면 소리나게 하니 중복적으로 계속나게됨)
- cnt사용하였지만 뚝뚝 끊기면서 문제가 있음, 영역을 벗어나면 다음음이 재생이 되게 바꿔야할듯 
     + 객체가 영역에 위치하는 경우 동작이 실행되고, 해당 객체가 영역을 벗어날 때까지 해당 동작이 다시 실행되지 않도록 하려면, 객체가 영역 내에 위치하는 상태를 저장하는 변수를 사용
- 소리가 하나일때는 잘 되는데 두개인 경우에는 안됨 -> 각각 1번 2번 정해서 변수를 다르게 해야할듯

>### TIL 
>-opencv에선 색상공간이 RGB가 아니라 >BGR이다. 빨간색 (0,0,255)



## 2023-04-11
### **중간예비점검**

   **idea**
   - 클릭하여 색 추출하도록
   - 손영역 전과 달라진것 추출
   - 장갑에 스티커 붙여서 색인식
   - 색옷입고 몸으로 치기 
   - 장갑 옷색 다르게 해서 각각 연주

   **tech**
   - 픽셀 경계 지정해서 그걸 따라가는 코드 있음
   - 'openCV 객체추적'이런식으로 검색.

   **문제점**
   - 밝기문제 : 창을 켜두었을때 hsv조절
   - 파이썬 언어 바꾸기 
   - 프로젝터 쓸것인지 
   - 카메라 위치 어떻게 할것인지 
- 

## 2023-04-15 
**solution?**
- 4area_division.py에서 영역에들어오면 소리 한번만 나게하는거 -> 조건을 여러개 해서 다 만족하면 play하도록


- fingetip.py 양손 손가락 끝점 표시( 좌표도 얻을 수 있음)
- 좌표 추출해봄 

<img src="https://user-images.githubusercontent.com/120040559/232230742-473ced31-db51-4e30-a1ea-dcbe0ea0babf.png" width="500"> 
<img src= https://user-images.githubusercontent.com/120040559/232230876-b6ae64c4-14f4-4fd8-b90b-7b4ed054a80e.JPG width="500"> 

인덱스를 추출한것인데 [엄지,검지,중지,약지,새끼] 순서


## 2023.04.19 
- Haar Cascade 검출기 사용해보기위해  OpenCV 깃허브 사이트에서 캐스케이드 학습되어진 특징 자료를 다운받음

## 2023.04.21 Zoom 미팅 예정 -> 취소 
**Question**
- 실행되기에 느린데 C++로 작성하면 좀 더 빠른지 
- 손가락 검출 방법 (손영역 전과 달라진것 추출, mediapipe, 컨투어 검출 )
- 손가락 말고 채를 인식하도록 하는것은 어떤지 ( 인식 방법으로 rgb 로 하는 방법이나 객체인식 haar cascade )
   + 손가락 포기하고 rgb 인식으로 간다면 장갑에 색깔 스티커 표시해서 손 추출하기 
   + 색옷입고 몸으로 치기 
- 만드는 목적에 대한 고민 
   + 카메라를 두개 쓰는 순간 편의성 면에서 의미가 없음 
-
-

## 2023.04.27 
미팅 전에 할것 
- 가운데쯤에 영역 나누고 들어오면 표시하기 
- 소리 한번만 나는거 고민해보기 

**한것**
5area_fingertip.py
- 가운데에 영역 5개로 나누고 손가락끝 들어오면 숫자로 표시되게함 

**할것**
- 소리나게 합치기 
- 건반영역 따오기 

## 2023.04.28 Zoom 미팅 예정
**Question**
1. 언어 무엇으로 사용할 것인가
2. depth 카메라 사용 유무(발열문제, 손가락 인식이 잘 안되기도 하고, 인식을 위한 거리가 꽤 길다)
3. 손가락 검출 방법  (손영역 전과 달라진것 추출, mediapipe, 컨투어 검출 )
4. 손가락 말고 채를 인식하도록 하는것은 어떤지 ( 인식 방법으로 rgb 로 하는 방법이나 객체인식 haar cascade)
   - 손가락 포기하고 rgb 인식으로 간다면 장갑에 색깔 스티커 표시해서 손 추출하기
   - 색옷입고 몸으로 치기(영역 옮겨다니면서 )
5. 만드는 목적 
- 카메라를 두개 쓰는 순간 편의성 면에서 의미가 없음
- 빔프로젝터도 편의성 면에서 의미가 없음 
- 따라서 빔 프로젝터 없이 사용가능한 프로그래밍 -> 시연할 때만 빔 프로젝터 이용
프로그램 시행할 때 건반이 준비되었는지 안 되었는지에 따라 실행시킴
6. 음악파일어떻게 실행 시키는지? 
- pygame(이건 키보드 이용할 때만 필요할 수도), simpleaudio 이용
7. 소리 파일 어디서 다운받는지 
 8. ((영역에 들어왔을때 소리 한번만 나게 해야하는데 어떤 알고리즘을 써야하는지?))

 **결과**
1. python 자체에 라이브러리가 있다 ->MIDI
2. 따라치게하고 정확도를 확인, 레슨 하는 식으로 난이도를 높인다
3. 좀 느린건 GPU노트북을 쓰거나 PC원격 서버로 보내서 클라우드 서버 사용
4. 옆에서 북을 칠 수 있게 

## 2023.05.03
**한것**

1. midi 파일 만들기  
2. midi 실행하는 코드 
3. draft에 파일 이름 리스트에 넣고 이벤트 발생하면 mid파일 실행하도록 수정
4. 중복 되는것 막기위해 변수도 넣고 해봄 

- v1.midi파일 만들어서 재생하는 (sleep문제있음)
- v2.만들어진 midi파일 재생(소리가 안남?)->play_music()함수안에 continue로 바꾸면 해결됨 
- v3.콜백 함수 써서 파란 원 영역들어오면 소리나도록 ( 다른영역가면 안남)

**idea**
1. callback 함수 쓰기 
      - play_music 함수가 실행되면, 해당 함수가 종료될 때까지 다음 코드가 실행되지 않도록 play_music 함수를 thread 형태로 실행하면 됩니다. 그리고 play_music 함수가 종료될 때, 상태를 변경하는 callback 함수를 호출하여 현재 실행 중인 음악 파일이 종료되었음을 알리고, 다음 음악 파일을 실행할 수 있도록 합니다.
2. flag 함수 써서 반복문 break로 빠져 나오기 
3. 음악 파일이 종료되기 전까지 새로운 음악 파일을 실행하지 않도록 하기 위해서는, 현재 실행 중인 음악 파일의 상태를 추적하고, 이 상태가 종료될 때까지 다른 음악 파일을 실행하지 않도록 해주기
4. 

**문제점**
1. 반복재생되는게 문제 

**고려할것**
1. 손가락, 드럼 한번에 어떻게 할지 
2. 인터페이스 어떻게 할지 
3. 건반 추출하기 


## 2023-05-05

(
device_id = pygame.midi.get_default_output_id()
print(device_id)

결과 : 0
)
1. play_mido : import mido, send(message) 이방법-> delay있음
2. play_note : 안에 sleep함수있어서 delay
   - while getbusy를 밖에다
3. play_music : 소리는 나는데 무한 반복

- wav사용하는 play는 동시 재생 가능한듯?

**한것**
1. 화음 만드는 파일 - make_harmony.py 
2. draft -> 양손 동시인식이 안된다?
   - for...위치 수정하니 해결됨
3. 영역 벗어나기 전까지 반복 안하도록 함 
   - 방법 : 
      >if event == prev_event:   
         flag = True   
         continue    
         추가하고 if문들 위치 수정 (들여쓰기)
4. 모든 손가락이 영역 벗어날때도 판별 하도록함 
   - 방법 :  
      >  if not is_object_in_any_area(location, areas) :   
      >           event = -1   
      >  object_location, areas):
   - > for area in areas:   
      >if is_object_in_area(object_location, area):   
      >   return True
    >return False"
    안됨 -> area[i]로 모든 영역 검사하는걸로 바꿔줌 -> 실패

## 2023-05-06
**GUI**
- Graphical User Interface
- **tkinter**
- exe파일 

**할것**
1. 소리나는 코드 넣기 
2. gui 

**한것**
1. 모든 손가락이 영역 벗어날때도 판별 하도록함
   - 방법 : outflag씀
   -> 같은 영역 연속으로 치는거 해결 
   -> 안됨? 엄지만 됨
2. event 마다 소리나게함

## 2023-05-07
1. 진지하게 고민 
fingertips =  [(245, 321), (235, 186), (175, 148), (133, 155), (62, 192)]
location =  (245, 321)
1
location =  (235, 186)
location =  (175, 148)
location =  (133, 155)
location =  (62, 192)
1
fingertips =  [(318, 257), (354, 161), (396, 206), (406, 320), (488, 233)]
location =  (318, 257)
location =  (354, 161)
location =  (396, 206)
location =  (406, 320)
3
location =  (488, 233)
3
fingertips =  [(393, 218), (439, 146), (491, 142), (525, 161), (567, 226)]
location =  (393, 218)
location =  (439, 146)
location =  (491, 142)
location =  (525, 161)
location =  (567, 226)
3

보면 
for 모든 손가락 위치
   print(위치)
   for 각 영역 (5개)
      if 영역에 들어가 있다면 
         print(영역) 
   -> 그위치가 영역에 들어가는지 검사하는 것  - 한손 손가락 두개가 다른 영역에 있으면 각각 표시됨

   -> 영역에 위치하는지 검사하는건 다를까?

   = 그럼.. event를.. 몇개씩 만들어야하나 cnt올려서 ?  event도 array인가 list만들어서 뭐뭐있나를 저장

   ->> 모든 손가락 나갔을때 out 출력하는거 성공 
   - 이제 같은 event면 다시 반복 안되게 하고 같은 영역이어도 인식하도록 

   -한손에 한손가락만 영역에 
   [1, 1]
[1]
[1]
[1, 1]
[1]
[1]
[1, 1]
[1]
[1]

- 한손 두 영역 
[1, 0, 1, 0]
[1, 0]
[1, 0]
[1, 0, 1, 0]
[1, 0]
[1, 0]

-양손 한영역
[]
[2]
[]
[2]
[]
[2]
[]
- 양손 한영역씩 
[2]
[1]
[2]
[1]
[2]
[1]
- 한손은 한영역, 한손은 두영역
[1, 0]
[2]
[1, 0]
[2]
[1, 0]
[2]
[1, 0]

- 양손일때와 한손일때 구별함 
