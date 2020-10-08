import pygame


class Ship:
    """管理飞船的类"""

    def __init__(self, ai_game):
        """初始化飞船属性及其初始位置"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.setting = ai_game.setting

        # 加载飞船图形并获取其外接矩形
        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()

        # 对于每一个新飞船， 都将其放在屏幕的最下方的中间位置
        self.rect.midbottom = self.screen_rect.midbottom

        # 在飞船的属性x,y中储存小数值
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # 移动标识符
        self.move_right = False
        self.move_left = False
        self.move_up = False
        self.move_down = False

    def update(self):
        """根据移动标识符的调整飞船的位置"""
        # 更新飞船而不是rect对象的x值
        if self.move_left and self.rect.left > 0:
            self.x -= self.setting.ship_speed
        if self.move_right and self.rect.right < self.screen_rect.right:
            self.x += self.setting.ship_speed
        if self.move_up and self.rect.top >0:
            self.y -= self.setting.ship_speed
        if self.move_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.setting.ship_speed

        # 根据 self.x 和 self.y 更新 self.rect.x 和 self.rect.y 的值
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)