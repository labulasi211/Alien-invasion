import pygame


class Ship:
    """管理飞船的类"""

    def __init__(self, ai_game):
        """初始化飞船属性及其初始位置"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # 加载飞船图形并获取其外接矩形
        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()

        # 对于每一个新飞船， 都将其放在屏幕的最下方的中间位置
        self.rect.midbottom = self.screen_rect.midbottom

        # 移动标识符
        self.move_right = False
        self.move_left = False

    def update(self):
        """根据移动标识符的调整飞船的位置"""
        if self.move_left:
            self.rect.x -= 1
        if self.move_right:
            self.rect.x +=1

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)