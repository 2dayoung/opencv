#비프음

from pynput import keyboard
import winsound
import time

# 1옥타브: C, C#, D, D#, E, F, F#, G, G#, A, A#, B
pitch = {'c_': 523, 'cs': 554, 'd_': 587, 'ds': 622, 'e_': 659,
         'f_': 698, 'fs': 740, 'g_': 784, 'gs': 831, 'a_': 880,
         'as': 932, 'b_': 988}
# 2옥타브
pitch2={}
for key, value in pitch.items():
    pitch2[key] = value * 2  # 한옥타브 위는 주파수가 2배.
print(pitch2)

# 지속시간
lasting = 3000

# time.sleep(2)
print("494")
winsound.Beep(555, lasting)
# time.sleep(2)
print("d")
winsound.Beep(pitch['d_'], lasting)


# # The event listener will be running in this block
# with keyboard.Events() as events:
#     for event in events:
#         if event.key == keyboard.Key.esc:
#             print("Exit!!")
#             break
#         elif event.key == keyboard.KeyCode(char='q'):
#             winsound.Beep(494, lasting)
#         elif event.key == keyboard.KeyCode(char='a'):
#             winsound.Beep(pitch['c_'], lasting)
#         elif event.key == keyboard.KeyCode(char='w'):
#             winsound.Beep(pitch['cs'], lasting)
#         elif event.key == keyboard.KeyCode(char='s'):
#             winsound.Beep(pitch['d_'], lasting)
#         elif event.key == keyboard.KeyCode(char='e'):
#             winsound.Beep(pitch['ds'], lasting)
#         elif (event.key == keyboard.KeyCode(char='d')) | (event.key == keyboard.KeyCode(char='r')):
#             winsound.Beep(pitch['e_'], lasting)
#         elif event.key == keyboard.KeyCode(char='f'):
#             winsound.Beep(pitch['f_'], lasting)
#         elif event.key == keyboard.KeyCode(char='t'):
#             winsound.Beep(pitch['fs'], lasting)
#         elif event.key == keyboard.KeyCode(char='g'):
#             winsound.Beep(pitch['g_'], lasting)
#         elif event.key == keyboard.KeyCode(char='y'):
#             winsound.Beep(pitch['gs'], lasting)
#         elif event.key == keyboard.KeyCode(char='h'):
#             winsound.Beep(pitch['a_'], lasting)
#         elif event.key == keyboard.KeyCode(char='u'):
#             winsound.Beep(pitch['as'], lasting)
#         elif (event.key == keyboard.KeyCode(char='j')) | (event.key == keyboard.KeyCode(char='i')):
#             winsound.Beep(pitch['b_'], lasting)
#         elif event.key == keyboard.KeyCode(char='k'):
#             winsound.Beep(pitch2['c_'], lasting)
#         elif event.key == keyboard.KeyCode(char='o'):
#             winsound.Beep(pitch2['cs'], lasting)
#         elif event.key == keyboard.KeyCode(char='l'):
#             winsound.Beep(pitch2['d_'], lasting)
#         elif event.key == keyboard.KeyCode(char='p'):
#             winsound.Beep(pitch2['ds'], lasting)
#         elif (event.key == keyboard.KeyCode(char=';')) | (event.key == keyboard.KeyCode(char='[')):
#             winsound.Beep(pitch2['e_'], lasting)
#         elif event.key == keyboard.KeyCode(char="'"):
#             winsound.Beep(pitch2['f_'], lasting)
#         elif event.key == keyboard.KeyCode(char="]"):
#             winsound.Beep(pitch2['fs'], lasting)

# # 빈 키(z,x,c,v... ) 에 대해 추가로 음계 할당
#         elif event.key == keyboard.KeyCode(char="z"):
#             winsound.Beep(pitch['c_'], lasting)
#         elif event.key == keyboard.KeyCode(char="x"):
#             winsound.Beep(pitch['d_'], lasting)
#         elif event.key == keyboard.KeyCode(char="c"):
#             winsound.Beep(pitch['e_'], lasting)
#         elif event.key == keyboard.KeyCode(char="v"):
#             winsound.Beep(pitch['f_'], lasting)
#         elif event.key == keyboard.KeyCode(char="b"):
#             winsound.Beep(pitch['g_'], lasting)
#         elif event.key == keyboard.KeyCode(char="n"):
#             winsound.Beep(pitch['a_'], lasting)
#         elif event.key == keyboard.KeyCode(char="m"):
#             winsound.Beep(pitch['b_'], lasting)
#         elif event.key == keyboard.KeyCode(char=","):
#             winsound.Beep(pitch2['c_'], lasting)
#         elif event.key == keyboard.KeyCode(char="."):
#             winsound.Beep(pitch2['d_'], lasting)
#         elif event.key == keyboard.KeyCode(char="/"):
#             winsound.Beep(pitch2['e_'], lasting)