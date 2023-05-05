#==============================================
#숫자키 1 2 3 4 에 도레미파.wav재생 
#개선 :  음원 끝날때 띡 소리가 남, 다른 소리도 추가
#pygame 이용
#==============================================
import mido

import pygame

pygame.init()


# open MIDI output port
outport = mido.open_output()



midi_filename = []
notes = [60, 62, 64, 65, 67, 69, 71]
for i, note in enumerate(notes):    
    midi_filename.append(str(note) +'.mid')
    
# open MIDI file
mid = mido.MidiFile(midi_filename[i])
# play MIDI messages
for message in mid.play():
    outport.send(message)


# 화면 크기 설정
size = [500, 300]
screen = pygame.display.set_mode(size)

# 창 제목 설정
pygame.display.set_caption("Play Sound with Keyboard")

# WAV 파일 디렉토리 경로
sounds_dir = "./sounds/"

# WAV 파일 로드
sound1 = pygame.mixer.Sound(sounds_dir + "1.wav")
sound2 = pygame.mixer.Sound(sounds_dir + "2.wav")
sound3 = pygame.mixer.Sound(sounds_dir + "3.wav")
sound4 = pygame.mixer.Sound(sounds_dir + "4.wav")

# 게임 루프
done = False
while not done:
    # 이벤트 루프
    for event in pygame.event.get():
        # 종료 이벤트 처리
        if event.type == pygame.QUIT:
            done = True
        # 키 이벤트 처리
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                mid = mido.MidiFile(midi_filename[1])
                # play MIDI messages
                for message in mid.play():
                    outport.send(message)
            elif event.key == pygame.K_2:
                mid1 = mido.MidiFile(midi_filename[2])
                # play MIDI messages
                for message in mid1.play():
                    outport.send(message)
            elif event.key == pygame.K_3:
                mid2 = mido.MidiFile(midi_filename[3])
                # play MIDI messages
                for message in mid2.play():
                    outport.send(message)
            elif event.key == pygame.K_4:
                mid3 = mido.MidiFile(midi_filename[4])
                # play MIDI messages
                for message in mid3.play():
                    outport.send(message)

    # 화면 업데이트
    pygame.display.flip()

# 종료
pygame.quit()
