import pygame

pygame.init()

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
                sound1.play()
            elif event.key == pygame.K_2:
                sound2.play()
            elif event.key == pygame.K_3:
                sound3.play()
            elif event.key == pygame.K_4:
                sound4.play()

    # 화면 업데이트
    pygame.display.flip()

# 종료
pygame.quit()
