import pygame
from random import randint

from pygame.sprite import Sprite


class Alien(Sprite):
    """表示单个外星人的类"""

    def __init__(self, ai_game):
        """初始化外星人并设置其初始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.setting = ai_game.setting
        self.points = 0

        # 加载外星人图像，并设置其rect属性
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # 每个外星人的初始位置都在屏幕右上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 储存外星人的基准水平位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # 外星人设置，由于每个外星人的参数都是随机的
        self.alien_speed = 0
        self.alien_drop_speed = 0
        # fleet_direction 为1表示外星人向右移，为-1表示外星人向左移
        self.alien_direction = 1

    def update(self):
        """向左，向右移动外星人"""
        self.x += (self.alien_speed * self.alien_direction)
        self.rect.x = self.x
        self.y += self.alien_drop_speed
        self.rect.y = self.y

    def check_edges(self):
        """如果外星人位于屏幕边缘，就返回True"""
        screen_width = self.setting.screen_width
        if self.rect.right >= screen_width or self.rect.left <= 0:
            return True
        else:
            return False