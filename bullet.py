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

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)


class BulletY(Bullet):
    """掌管飞船发射的Y轴方向的子弹额类"""

    def __init__(self, ai_game):
        """在飞船当前位置创建一个竖向子弹的类"""
        super().__init__(ai_game)

        # 在（0，0）的位置创建一个子弹矩阵，再将其设置到合适的位置
        self.rect = pygame.Rect(
            0, 0, self.setting.bullet_width, self.setting.bullet_height
        )

        # 判断子弹种类的标识符
        self.kinds = 0  # 0 -> Y轴正方向   1 -> X轴负方向   2 -> X轴正方向


class BulletYPositive(BulletY):
    """掌管飞船发射的Y轴正方向的子弹额类"""
    def __init__(self, ai_game):
        """初始化子弹发射位置，及其父类属性"""
        super().__init__(ai_game)
        self.rect.midtop = ai_game.ship.rect.midtop

        # 设置子弹方向属性
        self.kinds = 0

        # 储存用小数表示的子弹位置
        self.y = float(self.rect.y)

    def update(self):
        """向上移动子弹位置"""
        # 更新表示子弹位置的小数值
        self.y -= self.setting.bullet_speed
        # 更新表示子弹的 rect 的位置
        self.rect.y = self.y


class BulletX(Bullet):
    """掌管飞船X轴所发射子弹的类"""

    def __init__(self, ai_game):
        """在飞船当前位置创建一个横向子弹的类"""
        super().__init__(ai_game)

        # 在（0，0）的位置创建一个子弹矩阵
        self.rect = pygame.Rect(
            0, 0, self.setting.bullet_height, self.setting.bullet_width
        )



class BulletXNegative(BulletX):
    """创建一个横向向负方向射出的子弹类"""

    def __init__(self, ai_game):
        """初始化子弹发射位置，及其父类属性"""
        super().__init__(ai_game)

        # 将横向负方向移动的子弹设置到合适的位置
        self.rect.midleft = ai_game.ship.rect.midleft

        # 设置子弹方向属性
        self.kinds = 1

        # 储存用小数表示的子弹位置
        self.x = float(self.rect.x)

    def update(self):
        """向x轴负方向移动子弹位置"""
        # 更新表示子弹位置的小数值
        self.x -= self.setting.bullet_speed
        # 更新表示子弹的 rect 的位置
        self.rect.x = self.x


class BulletXPositive(BulletX):
    """创建一个横向向负方向射出的子弹类"""

    def __init__(self, ai_game):
        """初始化子弹发射位置，及其父类属性"""
        super().__init__(ai_game)

        # 将横向负方向移动的子弹设置到合适的位置
        self.rect.midright = ai_game.ship.rect.midright

        # 设置子弹方向属性
        self.kinds = 2

        # 储存用小数表示的子弹位置
        self.x = float(self.rect.x)

    def update(self):
        """向x轴负方向移动子弹位置"""
        # 更新表示子弹位置的小数值
        self.x += self.setting.bullet_speed
        # 更新表示子弹的 rect 的位置
        self.rect.x = self.x
