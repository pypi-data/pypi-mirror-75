# encoding: utf-8
import os
import random
import sys

import pygame
from pygame.locals import *



#-------------------------------------------------------------------------
# 函數:秀字.
#-------------------------------------------------------------------------
def showFont( text, x, y, color):
    global canvas    
    text = font.render(text, True, color) 
    canvas.blit( text, (x,y))

#-------------------------------------------------------------------------
# 函數:碰撞判斷.
#   x       : x 
#   y       : y 
#   boxRect : 矩形
#-------------------------------------------------------------------------
def isCollisionUD( x, y, boxRect):
    if (x >= boxRect[0] and x <= boxRect[0] + boxRect[2]):
        if((y >= boxRect[1] + boxRect[3]-7 and y <= boxRect[1] + boxRect[3])or (y >= boxRect[1] and y <= boxRect[1] +7)):
            return True;          
    return False;
def isCollisionLR( x, y, boxRect):
    if (y >= boxRect[1] and y <= boxRect[1] + boxRect[3]):
        if((x >= boxRect[0] and x <= boxRect[0] +7) or (x >=boxRect[0] + boxRect[2]-7 and x <= boxRect[0] + boxRect[2])):
            return True;          
    return False;

#-------------------------------------------------------------------------
# 函數:初始遊戲.
#-------------------------------------------------------------------------
def resetGame():
    # 宣告使用全域變數.
    global game_mode, brick_num, bricks_list, dx, dy, ball_num,win
    pinkList = [14,18,24,25,26,28,29,30,34,35,36,37,38,39,40,41,42,45,46,47,48,49,50,51,52,53,56,57,58,59,60,61,62,63,64,67,68,69,70,71,72,73,74,75,79,80,81,82,83,84,85,91,92,93,94,103,104,105,115]
    # 磚塊
    for i in range(len(bricks_list)):
        # 亂數磚塊顏色
        blue = 127,255,212
        pink = 255,192,203
        if( i in pinkList):
            bricks_list[i].color = pink
        else:
            bricks_list[i].color = blue    
        # 開啟磚塊.
        bricks_list[i].visible = True
    # 0:等待開球
    game_mode = 0
    # 磚塊數量.
    brick_num = 132    
    # 移動速度.
    dx =  6*random.choice([-1,1])
    dy = -6*random.choice([-1,1])
    ball_num=10

class Box(object):
    def __init__( self, pygame, canvas, name, rect, color):
        self.pygame = pygame
        self.canvas = canvas
        self.name = name
        self.rect = rect
        self.color = color
        self.visible = True
        
    def update(self):
        if(self.visible):
            
            self.pygame.draw.rect( self.canvas, self.color, self.rect)

class Button(object):
    def __init__(self,pygame,canvas,name,rect,color):
        self.pygame=pygame
        self.canvas = canvas
        self.name = name
        self.rect = rect
        self.color = color
        self.visible = False
        self.screen_rect = canvas.get_rect()
        self.text_color=(255,255,255)
        self.font = pygame.font.SysFont(None,30)
        
    def update(self):
        if(win ==0):
            msg = "Retry Again"
        else:
            msg = "psd:30HBD"
        if(self.visible):
            self.msg_img = self.font.render(msg,True,self.text_color,self.color)
            self.msg_img_rect = self.msg_img.get_rect()
            self.msg_img_rect.center = (340,340)
            self.canvas.fill(self.color,self.rect)
            self.canvas.blit(self.msg_img,self.msg_img_rect)
            
            #self.pygame.draw.rect(self.canvas,self.color,self.rect)

#-------------------------------------------------------------------------
# 畫圓.
#-------------------------------------------------------------------------
class Circle(object):
    def __init__( self, pygame, canvas, name, pos, radius, color):
        self.pygame = pygame
        self.canvas = canvas
        self.name = name
        self.pos = pos
        self.radius = radius
        self.color = color
        
        self.visible = True


    def update(self):
        if(self.visible):
            self.pygame.draw.circle( self.canvas, self.color, self.pos , self.radius)

if __name__ =="__main__":
# 視窗大小.
canvas_height = 680
canvas_width = 680

# 顏色.
black = (0,0,0)

# 磚塊數量串列.
bricks_list = []

# 移動速度.

dx =  6*random.choice([-1,1])
dy = -6*random.choice([-1,1])

# 遊戲狀態.
# 0:等待開球
# 1:遊戲進行中
game_mode = 0
# 初始.
pygame.init()
# 顯示Title.
pygame.display.set_caption(u"打磚塊遊戲")
# 建立畫佈大小.
canvas = pygame.display.set_mode((canvas_width, canvas_height))
# 時脈.
clock = pygame.time.Clock()

# 設定字型.
font = pygame.font.SysFont("simsunnsimsun", 18)

# 底板.
paddle_x = 0
paddle_y = (canvas_height - 48)
paddle = Box(pygame, canvas, "paddle", [paddle_x, paddle_y, 100, 24], (255,255,255))

win =0
# 球.
ball_num=10
ball_x = paddle_x
ball_y = paddle_y
ball   = Circle(pygame, canvas, "ball", [ball_x, ball_x], 8, (255,255,255))

retry_but = Button(pygame,canvas,"retry",[340-70,315,140,50],(255,179,230))

# 建立磚塊
brick_num = 0
brick_x = 10
brick_y = 30
brick_w = 0
brick_h = 0
for i in range( 0, 132):
    if((i % 11)==0):
        brick_w = 0
        brick_h = brick_h + 30        
    bricks_list.append (Box(pygame, canvas, "brick_"+str(i), [  brick_w + brick_x, brick_h+ brick_y, 59.5, 29], [255,255,255]))
    brick_w = brick_w + 60
# 初始遊戲.
resetGame()
img = pygame.image.load(os.path.join(os.path.dirname(__file__),"cover.jpg"))
img.convert()

#-------------------------------------------------------------------------    
# 主迴圈.
#-------------------------------------------------------------------------
running = True
while running:      
    #---------------------------------------------------------------------
    # 判斷輸入.
    #---------------------------------------------------------------------
    for event in pygame.event.get():
        # 離開遊戲.
        if event.type == pygame.QUIT:
            running = False
        # 判斷按下按鈕
        if event.type == pygame.KEYDOWN:
            # 判斷按下ESC按鈕
            if event.key == pygame.K_ESCAPE:
                running = False
                    
        # 判斷Mouse.
        if event.type == pygame.MOUSEMOTION:
            paddle_x = pygame.mouse.get_pos()[0] - 50
        if event.type == pygame.MOUSEBUTTONDOWN:
            if(game_mode == 0):
                game_mode = 1
            elif(game_mode==2):
                if(340+70>pygame.mouse.get_pos()[0]>340-70 and 340+25>pygame.mouse.get_pos()[1]>315):
                    if(win==0):
                        game_mode==0
                        resetGame()
                    else:
                        running = False
                        

    #---------------------------------------------------------------------    
    # 清除畫面.
    canvas.fill(black)
    canvas.blit(img,(120,60))
    # 磚塊
    for bricks in bricks_list:
        # 球碰磚塊.
        if(isCollisionUD( ball.pos[0], ball.pos[1], bricks.rect)):
            if(bricks.visible):                
                # 扣除磚塊.
                brick_num = brick_num -1
                # 初始遊戲.
                if(brick_num <= 0):
                    win=1
                    game_mode=2
                    #resetGame()
                    #break
                # 球反彈.
                dy = -dy; 
            # 關閉磚塊.
            bricks.visible = False
        elif(isCollisionLR( ball.pos[0], ball.pos[1], bricks.rect)):
            if(bricks.visible):                
                # 扣除磚塊.
                brick_num = brick_num -1
                # 初始遊戲.
                if(brick_num <= 0):
                    win=1
                    game_mode=2
                    #resetGame()
                    break
                # 球反彈.
                dx = -dx; 
            # 關閉磚塊.
            bricks.visible = False
        # 更新磚塊.        
        bricks.update()
                
    #顯示磚塊數量.
    showFont( u"剩餘球數:"+str(ball_num), 8, 20, (255, 0, 0))

    # 秀板子.
    paddle.rect[0] = paddle_x
    paddle.update()

    # 碰撞判斷-球碰板子.
    if(isCollisionUD( ball.pos[0], ball.pos[1], paddle.rect)):        
        # 球反彈.
        dy = -dy;         
                
    # 球.
    # 0:等待開球
    if(game_mode == 0):
        ball.pos[0] = ball_x = paddle.rect[0] + ( (paddle.rect[2] - ball.radius) >> 1 )
        ball.pos[1] = ball_y = paddle.rect[1] - ball.radius        
    # 1:遊戲進行中
    elif(game_mode == 1):
        ball_x += dx
        ball_y += dy
        #判斷死亡.
        if(ball_y + dy > canvas_height - ball.radius):
            game_mode = 0      
            ball_num-=1
            if(ball_num<=0):
                game_mode=2

        # 右牆或左牆碰撞.
        if(ball_x + dx > canvas_width - ball.radius or ball_x + dx < ball.radius):
            dx = -dx
        # 下牆或上牆碰撞
        if(ball_y + dy > canvas_height - ball.radius or ball_y + dy < ball.radius):        
            dy = -dy
        ball.pos[0] = ball_x
        ball.pos[1] = ball_y
    elif(game_mode==2):
        #print("game over")
        retry_but.visible=True
        if(340+70>pygame.mouse.get_pos()[0]>340-70 and 340+25>pygame.mouse.get_pos()[1]>340-25):
            retry_but.color=(221,160,221)
        else:
            retry_but.color = (255,179,230)
        retry_but.update()

    # 更新球.
    ball.update()
        
    # 顯示中文.
    showFont( u"FPS:" + str(int(clock.get_fps())), 8, 2, (255, 0, 0))

    # 更新畫面.
    pygame.display.update()
    clock.tick(60)

# 離開遊戲.
pygame.quit()
if(win==1):
    fl = open("C:/check.txt","w")
    fl.write("psd:30HBD")
    fl.close()
    
if(win==0):
    fl = open("C:/fail.txt","w")
    fl.write("psd:30HBD")
    fl.close()
quit()
