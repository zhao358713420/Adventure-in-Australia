import random
import time

import pygame
import serial

#-------------------窗口参数设置-----------------------
display_width = 900  #窗口宽度
display_height = 600  #窗口高度
game_display = None  #窗口对象
clock = None  #计时
start = time.clock()

#-------------------颜色定义----------------------
black = (0, 0, 0)  #黑色
white = (255, 255, 255)  #白色
red = (200, 0, 0)  #红色
green = (0, 200, 0)  #绿色
yellow = (255,255,0) #黄色
bright_red = (255, 0, 0)  #亮红色
bright_green = (0, 255, 0)  #亮绿色

#-------------------初始化---------------------
pygame.init()
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('FlappyBird')
clock = pygame.time.Clock()

#-------------------游戏参数设置-----------------
jump_sound = pygame.mixer.Sound("./Src/jump.wav")
crash_sound = pygame.mixer.Sound("./Src/crash.wav")
crash_flag = 0
time_count = 0.000
time_flag = 0.000
bird_x = 200
bird_y = 500
bird_height = 50
bird_weight = 50
block_gap = 100  #阻碍物之间的间隔
block_width = 100
bird_x_speed = 4
jump_speed = 3
fall_speed = 2
map_x = 0
ground = 500
ground_map = []
i = 0
is_jump = False
jump_num = 0
block1_x = 950
block1_height_1 = 2
block1_height_2 = 1
block2_x = 1500
block2_height_1 = 1
block2_height_2 = 3
close = None
bird_image1 = pygame.image.load('./Src/1.jpg')
bird_image2 = pygame.image.load('./Src/2.jpg')
cactus_image1 = pygame.image.load('./Src/cactus1.png')
cactus_image2 = pygame.image.load('./Src/cactus2.png')
cactus_image3 = pygame.image.load('./Src/cactus3.png')
start_image = pygame.image.load('./Src/start.jpg')
bird_no = 1
while i <  900:
    for j in range(i,i + 11):
        ground_map.append(1)
    for j in range(i+11,i+21):
        ground_map.append(0)
    i += 20 
score = 0
block1_score = True
block2_score = True
#################链接arduino#########

ser = serial.Serial('COM3', 9600)
#随机生成
def draw_block(x,height1,height2):
    pygame.draw.rect(game_display,black,((x,0),(100,height1)),0)
    pygame.draw.rect(game_display,black,((x,550-height2),(100,height2)),0)

# def draw_block(x,y):
#     pygame.draw.rect(game_display,black,((x,y),(100,550-y)),0)

def draw_ground(map_x):
    for i in range(map_x,map_x+display_width):
        if ground_map[i % display_width] == 0:
            pygame.draw.aaline(game_display,black,(i-map_x,550),(i-map_x,550))
        else :
            pygame.draw.aaline(game_display,black,(i-map_x,555),(i-map_x,555))

def draw_bird():
    global bird_x
    global bird_y
    global bird_no
    global is_jump
    if not is_jump and bird_y < ground:
        bird_y += fall_speed
    if bird_y > ground:
        bird_y = ground
    if not is_jump:
        game_display.blit(bird_image2,(bird_x,bird_y))
    else:
        game_display.blit(bird_image1,(bird_x,bird_y))

def draw_bird2():
    global bird_x
    global bird_y
    global bird_no
    global is_jump
    # if not is_jump and bird_y < ground:
    #     bird_y += fall_speed
    # if bird_y > ground:
    #     bird_y = ground
    if not is_jump:
        game_display.blit(bird_image2,(bird_x,bird_y))
    else:
        game_display.blit(bird_image1,(bird_x,bird_y))
   
def init():
    global bird_x,bird_y,time_count,time_flag,start,bird_x_speed
    global block1_x,block1_height_1,block1_height_2,block2_x,block2_height_1,block2_height_2
    global map_x,is_jump,jump_num,block1_score,block2_score,score
    bird_x = 200
    bird_y = 500
    block1_x = 950
    block1_height_1 = 2
    bird_x_speed = 4
    block1_height_2 = 1
    block2_x = 1500
    block2_height_1 = 1
    map_x = 0
    is_jump = False
    jump_num = 0
    score = 0
    block1_score = True
    block2_score = True
    time_count = 0.000
    time_flag = 0.000
    start = time.clock()
    global crash_flag
    crash_flag = 0
block2_height_2 = 3 
def draw(map_x):
    draw_ground(map_x)
    draw_bird()
    draw_move()

def draw_2(map_x):
    draw_ground(map_x)
    draw_bird2()

def draw_move():
    global map_x
    global ground
    global bird_y
    global fall_speed

    if bird_y != ground:
        if not is_jump or jump_num > 2:
            if bird_y <= ground:
                bird_y += fall_speed
                fall_speed += 0.3
                if bird_y >ground:
                    bird_y = ground
                    global jump_num
                    jump_num = 0
                    fall_speed = 2
        elif is_jump:
            bird_y -= jump_speed
            bird_x += 2
    else:
        global jump_num
        jump_num = 0
        fall_speed = 2
        global bird_x 
        if bird_x > 200:
            bird_x -= 1
    if is_jump:
        bird_y -= jump_speed

def jump():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(jump_sound)
    pygame.mixer.music.stop()
    global is_jump
    global jump_num
    if jump_num >= 0 and jump_num < 1:
        is_jump = True
        jump_num += 1

    
def text_objects(text, font):
    textSurface = font.render(text, True, red)
    return textSurface, textSurface.get_rect()
 
def message_display(text,x,y,num):
    largeText = pygame.font.Font('./Src/LucidaBrightDemiBold.ttf',num)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (x,y)
    game_display.blit(TextSurf, TextRect)

def draw_cactus(x,height1,height2):
    for i in range(height2):
        game_display.blit(cactus_image3,(x+32,550-20*(i+1)))
    game_display.blit(cactus_image2,(x,550-20*height2 - 122))
    for i in range(height1):
        game_display.blit(cactus_image3,(x+32,20*(i)))
    game_display.blit(cactus_image1,(x,20*(height1)))
    
def is_crash():
    global block1_x,block1_height_1,block1_height_2,block2_x,block2_height_1,block2_height_2
    global bird_x,bird_y,score
    if not (bird_x > block1_x + 100 or bird_x + 35 < block1_x ):
        if bird_y < block1_height_1*20+122 or bird_y + 35 > 550 - block1_height_2*20 - 122 :
            print("block 1 error"+str(score))
            print("birds:x:"+str(bird_x)+"y:"+str(bird_y))
            print("block1:x:"+str(block1_x)+"h1:"+str(block1_height_1)+"h2:"+str(block1_height_2))
            print("block2:x:"+str(block2_x)+"h1:"+str(block2_height_1)+"h2:"+str(block2_height_2))
            return True
    if not (bird_x > block2_x + 100 or bird_x + 50 < block2_x ):
        if bird_y < block2_height_1*20+122 or bird_y + 35 > 550 - block2_height_2*20 - 122 :
            print("block 2 error"+str(score))
            print("birds:x:"+str(bird_x)+"y:"+str(bird_y))
            print("block1:x:"+str(block1_x)+"h1:"+str(block1_height_1)+"h2:"+str(block1_height_2))
            print("block2:x:"+str(block2_x)+"h1:"+str(block2_height_1)+"h2:"+str(block2_height_2))
            return True
    
def crash():
    global crash_flag
    if crash_flag == 0:
        pygame.mixer.music.stop()
        pygame.mixer.Sound.play(crash_sound)
        pygame.mixer.music.stop()
    crash_flag += 1
    message_display("YOU ARE DEAD!",display_width/2,display_height/2,40)
    
def loop2():
    quit_flag2 = False
    global time_count,score
    while not quit_flag2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    quit_flag2 = True
                    quit_flag1 = False
                    init()
                    game_loop()
                    break
        if arduinoLoop2():
            quit_flag2 = True
            quit_flag1 = False
            init()
            game_loop()
            break
        game_display.fill(white)
        draw_2(map_x)
        draw_cactus(block1_x,block1_height_1,block1_height_2)
        draw_cactus(block2_x,block2_height_1,block2_height_2)

        crash()
        message_display("score : "+str(score),50,50,15)
        message_display("time : "+str(time_count),68,70,15)
        # quit_flag2 = True
        pygame.display.update()
        # time.sleep(2)
        # clock.tick(80)

def arduinoLoop():
    line = ""
    while len(line) == 0:
        line = ser.readline()
    data = [int(val) for val in line.split()]
    print(data)
    button_flag = False
    try:
        if data[0] ==1:
            button_flag = True
    except IndexError:
        button_flag = False
    return button_flag

def arduinoLoop2():
    line = ""
    while len(line) == 0:
        line = ser.readline()
    data = [int(val) for val in line.split()]
    print(data)
    button_flag = False
    try:
        if data[1] ==1:
            button_flag = True
    except IndexError:
        button_flag = False
    return button_flag

#游戏循环
def game_loop():
    global block1_x,block1_height_1,block1_height_2,block2_x,block2_height_1,block2_height_2
    quit_flag1 = False
    quit_flag2 = True
    while not quit_flag1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    jump()
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    global is_jump
                    is_jump = False
        # print(arduinoLoop)
        if arduinoLoop():
            jump()
        else:
            global is_jump
            is_jump = False
        game_display.fill(white)
        if is_crash():
            quit_flag1 = True
            quit_flag2 = False
            loop2()
            break
        global map_x
        draw(map_x)
        draw_cactus(block1_x,block1_height_1,block1_height_2)
        draw_cactus(block2_x,block2_height_1,block2_height_2)
        # draw_block(block1_x,block1_height_1,block1_height_2)
        # draw_block(block2_x,block2_height_1,block2_height_2)
        global bird_x_speed
        map_x += bird_x_speed
        block1_x -= bird_x_speed
        block2_x -= bird_x_speed
        global score,block1_score,block2_score
        if block1_x + 100 <= 0:
            block1_height_1 = random.randint(1,5)
            block1_height_2 = random.randint(1,5)
            if block2_x < display_width:
                block1_x = display_width + 50
                block1_score = True
            else:
                block1_x = block2_x + 200
                block1_score = True
        if block2_x + 100 <= 0:
            block2_height_1 = random.randint(1,5)
            block2_height_2 = random.randint(1,5)
            if block1_x < display_width:
                block2_x = display_width + 50
                block2_score = True
            else:
                block2_x = block1_x + 150
                block2_score = True
        if block1_x + 100 < bird_x and block1_score:
            score += 1
            block1_score = False
        if block2_x + 100 < bird_x and block2_score:
            score += 1
            block2_score = False
        message_display("score : "+str(score),50,50,15)
        global time_count
        time_count = float(time.clock()) - float(start)
        time_count = "%.4f" % time_count
        message_display("time : "+str(time_count),68,70,15)
        global time_flag
        if float(time_count) - time_flag == 5.000:
            bird_x_speed += 2
            time_flag = time_count
        pygame.display.update()
        # clock.tick(80)

def start1():
    # game_display.fill(white)
    game_display.blit(start_image,(0,0))
    # draw_2(map_x)
    # draw_cactus(block1_x,block1_height_1,block1_height_2)
    # draw_cactus(block2_x,block2_height_1,block2_height_2)
    pygame.display.update()
    # message_display("as",display_width/2,display_height/2,80)
    # pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if arduinoLoop2():
            return True

flag = start1()   
if flag:
    game_loop()
# while True:
#     print(arduinoLoop())
