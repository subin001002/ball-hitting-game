import pygame           # pygame Load
import sys              # System Lib Load
import random           # Random Load
from time import sleep  # Time

padWidth = 480     # Game Width Size
padHeight = 640    # Game Height Size
rockImage = ['images/rock01.png', 'images/rock02.png', 'images/rock03.png', 'images/rock04.png', 'images/rock05.png', \
             'images/rock06.png', 'images/rock07.png', 'images/rock08.png', 'images/rock09.png', 'images/rock10.png', \
             'images/rock11.png', 'images/rock12.png', 'images/rock13.png', 'images/rock14.png', 'images/rock15.png', \
             'images/rock16.png', 'images/rock17.png', 'images/rock18.png', 'images/rock19.png', 'images/rock20.png', \
             'images/rock21.png', 'images/rock22.png', 'images/rock23.png', 'images/rock24.png', 'images/rock25.png', \
             'images/rock26.png', 'images/rock27.png', 'images/rock28.png', 'images/rock29.png', 'images/rock30.png']
explosionSound = ['sound/explosion01.wav', 'sound/explosion02.wav', 'sound/explosion03.wav', 'sound/explosion04.wav' ]


# 운석을 맞춘 개수 Count
def writeScore(count):
    global gamePad
    font = pygame.font.Font('font/NanumGothic.ttf', 20)
    text = font.render('파괴한 운석 수:' + str(count), True, (255, 255, 255))
    gamePad.blit(text,(10,0))

# 운석이 화면 아래로 통과한 Count
def writePassed(count):
    global gamePad
    font = pygame.font.Font('font/NanumGothic.ttf', 20)
    text = font.render('놓친 운석 :' + str(count), True, (255, 0, 0))
    gamePad.blit(text, (350,0))

# 게임 메시지 출력
def writeMessage(text):
    global gamePad, gameoverSound
    textfont = pygame.font.Font('font/NanumGothic.ttf', 80)
    text = textfont.render(text, True, (255, 0, 0))
    textpos = text.get_rect()
    textpos.center = (padWidth/2, padHeight/2)
    gamePad.blit(text, textpos)
    pygame.display.update()
    pygame.mixer.music.stop()       # 배경 음악 정지
    gameoverSound.play()            # 게임 오버 사운드 재생
    sleep(2)
    pygame.mixer.music.play(-1)     # 배경 음악 재생
    runGame()

# 전투기가 운석과 충돌했을 때 메시지 출력
def crash():
    global gamePad
    writeMessage('전투기 파괴!')

# 게임 오버 메시지 보기
def gameOver():
    global gamePad
    writeMessage('게임 오버!')

#Gmae Object Drawing
def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))   # blit란 비티 현상과 관련하여 해당하는 오브젝트를 x,y좌표 위치로 부터 그려라 라는 의미
    
#Game Reset
def initGame():
    global gamePad, clock, background, fighter, missile, explosion, missileSound, gameoverSound       # global 변수 호출
    pygame.init()                                                           # Lib 초기화
    gamePad = pygame.display.set_mode((padWidth, padHeight))                # 게임 전체 크기 정의
    pygame.display.set_caption('PyShooting_Cho_Exam')                       # 게임 이름 정의
    background = pygame.image.load('images/background.png')                 # 배경 이미지
    fighter = pygame.image.load('images/fighter.png')                       # 전투기 이미지
    missile = pygame.image.load('images/missile.png')                       # 미사일 이미지
    explosion = pygame.image.load('images/explosion.png')                   # 폭발 그림
    pygame.mixer.music.load('sound/music.wav')                              # 배경 음악
    pygame.mixer.music.play(-1)                                             # 배경 음악 재생
    missileSound = pygame.mixer.Sound('sound/missile.wav')                  # 미사일 사운드
    gameoverSound = pygame.mixer.Sound('sound/gameover.wav')                # 게임 오버 사운드
    clock = pygame.time.Clock()

#Game Start
def runGame():
    global gamepad, clock, background, fighter, missile, explosion, missileSound

    # 전투기 Size
    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]

    # 전투기 초기 위치 (x, y)
    x = padWidth * 0.45
    y = padHeight * 0.9
    fighterX = 0

    # 미사일 좌표 리스트
    missileXY = []

    # 운석 랜덤 생성
    rock = pygame.image.load(random.choice(rockImage))  #랜덤하게 30개 중 하나의 운석을 고름
    rockSize = rock.get_rect().size                     #운석 크기
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]
    destroySound = pygame.mixer.Sound(random.choice(explosionSound))

    # 운석 초기 위치 설정
    rockX = random.randrange(0, padWidth - rockWidth)
    rockY = 0
    rockSpeed = 2
    
    # 전투기 미사일에 운석이 맞았을 경우 True
    isShot = False
    shotCount = 0
    rockPassed = 0

    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:     # 게임 프로그램 종료
                pygame.quit()
                sys.exit()                      # 창을 닫거나 하면 게임을 종료시키고 시스템 종료 시키는 이벤트

            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT:      # 전투기 왼쪽으로 이동
                    fighterX -= 5

                elif event.key == pygame.K_RIGHT:   # 전투기 오른쪽으로 이동
                    fighterX += 5
                    
                elif event.key == pygame.K_SPACE:   # 미사일 발사
                    missileSound.play()
                    missileX = x + fighterWidth/2   # 현재 비행기의 중간부분에서 나가게끔 x좌표를 잡아
                    missileY = y - fighterHeight    # 비행기의 세로 부분만큼 빼주면 비행기 앞부분에서 미사일이 나감
                    missileXY.append([missileX, missileY])
                    
            if event.type in [pygame.KEYUP]:        # 방향키를 떼면 전투기 멈
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighterX = 0
        

        drawObject(background, 0, 0)            # 배경화면 그리기

        # 전투기 위치 재조정
        x += fighterX
        if x < 0:
            x = 0
        elif x > padWidth - fighterWidth:       # 게임 좌측으로 빠져나갈 수 없도록 최대치 지정
            x = padWidth - fighterWidth         # 게임 우측으로 빠져나갈 수 없게 막아주기

        # 전투기가 운석과 충돌했는지 체크
        if y < rockY + rockHeight:
            if(rockX > x and rockX < x + fighterWidth) or \
                     (rockX + rockWidth > x and rockX + rockWidth < x + fighterWidth):
                crash()

        drawObject(fighter, x, y)               # 비행기를 게임 화면의 (x, y)좌표에 그리

        # 미사일 발사 화면에 그리기
        if len(missileXY) != 0:                 # 비행기의 Length를 구한다. 그리고 1개 이상일 경우 조건에 따라서 미사일을 그
            for i, bxy in enumerate(missileXY): # 미사일 요소에 대해 반복함
                bxy[1] -= 10                    # 총알의 y좌표 -10 (위로 이동)
                missileXY[i][1] = bxy[1]

                if bxy[1] < rockY:
                    if bxy[0] > rockX and bxy[0] < rockX + rockWidth:
                        missileXY.remove(bxy)
                        isShot = True
                        shotCount += 1
                
                if bxy[1] <= 0:
                    try:
                        missileXY.remove(bxy)
                    except:
                        pass
                    
        if len(missileXY) != 0:
            for bx, by in missileXY:
                drawObject(missile, bx, by)

        # 운석 맞춘 점수 표시
        writeScore(shotCount)

        rockY += rockSpeed                      # 운석 아래로 움직임

        # 운석이 지구로 떨어진 경우
        if rockY > padHeight:
            # 새로운 운석 (랜덤)
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            rockPassed += 1

        if rockPassed == 3:
            gameOver()

        writePassed(rockPassed)

        if isShot:
            drawObject(explosion, rockX, rockY) #운석 폭발 그리기
            destroySound.play() #운석 폭발 사운드 재생
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            destroySound = pygame.mixer.Sound(random.choice(explosionSound))
            isShot = False

            #운석 맞추면 속도 증가
            rockSpeed += 0.02
            if rockSpeed >= 10:
                rockSpeed = 10
            

        drawObject(rock, rockX, rockY)          # 운석 그리
            
        pygame.display.update()                 # 게임화면을 Update
        clock.tick(60)                          # 게임화면의 초당 프레임수를 60으로 설정

    pygame.quit() # pygame 종료


#위의 정의된 initGame과 runGame을 실행
initGame()
runGame()
                
