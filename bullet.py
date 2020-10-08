import pygame

from pygame.sprite import Sprite


class Bullet(Sprite):
    """掌管飞船所发射子弹的类"""

    def __init__(self, ai_game):
        """在飞船当前位置创建一个子弹的类"""
        super().__init__()
        self.screen = ai_game.screen
        self.setting = ai_game.setting
        self.color = self.setting.bullet_color

        # 在（0，0）的位置创建一个子弹矩阵，再将其设置到合适的位置
        self.rect = pygame.Rect(
            0, 0, self.setting.bullet_width, self.setting.bullet_height
        )
        self.rect.midtop = ai_game.ship.rect.midtop

        # 储存用小数表示的子弹位置
        self.y = float(self.rect.y)

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)

    def update(self):
        """向上移动子弹位置"""
        # 更新表示子弹位置的小数值
        self.y -= self.setting.bullet_speed
        # 更新表示子弹的 rect 的位置
        self.rect.y = self.y
