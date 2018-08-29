import pygame
import sys

# 初始化Pygame
pygame.init()

size = width, height = 600, 400


# 创建指定大小的窗口 Surface
screen = pygame.display.set_mode(size)
# 设置窗口标题
pygame.display.set_caption("冯小雨")
bg = (0,0,0)

font = pygame.font.Font(None,20)#设置字体
line_height = font.get_linesize() #设置高度
position = 0#让　位置为0

screen.fill(bg)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        screen.blit(font.render(str(event),True,(0,255,0)),(0,position))
        position += line_height
        if position >height:
            position = 0
            screen.fill(bg)
    pygame.display.flip()#刷新页面
