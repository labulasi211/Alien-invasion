import sys

import pygame

from setting import Setting

from ship import Ship


class AlienInvasion:
    """管理游戏资源和行为得类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.setting = Setting()

        self.screen = pygame.display.set_mode(
            (self.setting.screen_width, self.setting.screen_high)
        )
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)

    def run_game(self):
        """开始游戏得主循环"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_screen()

    def _check_events(self):
        """监视键盘和鼠标得事件"""
        for even in pygame.event.get():
            if even.type == pygame.QUIT:
                sys.exit()
            elif even.type == pygame.KEYDOWN:
                if even.key == pygame.K_RIGHT:
                    # 向右移动飞船
                    self.ship.move_right = True
                elif even.key == pygame.K_LEFT:
                    # 向左移动飞船
                    self.ship.move_left = True
            elif even.type == pygame.KEYUP:
                # 停止移动
                if even.key == pygame.K_RIGHT:
                    self.ship.move_right = False
                elif even.key == pygame.K_LEFT:
                    self.ship.move_left = False

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        # 每次循环都会重绘屏幕
        self.screen.fill(self.setting.bg_color)
        self.ship.blitme()

        # 让最近绘制得屏幕可见
        pygame.display.flip()


if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
