import sys

import pygame

from setting import Setting

from ship import Ship

from bullet import Bullet


class AlienInvasion:
    """管理游戏资源和行为得类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.setting = Setting()

        self.screen = pygame.display.set_mode((900, 600))
        self.setting.screen_height = self.screen.get_rect().height
        self.setting.screen_width = self.screen.get_rect().width
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

    def run_game(self):
        """开始游戏得主循环"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()

    def _check_events(self):
        """监视键盘和鼠标得事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                print(event.key)
                self._check_keydown_event(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        # 每次循环都会重绘屏幕
        self.screen.fill(self.setting.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # 让最近绘制得屏幕可见
        pygame.display.flip()

    def _check_keydown_event(self, event):
        """响应按键"""
        if event.key == pygame.K_SPACE:
            # 发射子弹
            self.setting.fire_bullet = True
        elif event.key == pygame.K_RIGHT:
            # 向右移动飞船
            self.ship.move_right = True
        elif event.key == pygame.K_LEFT:
            # 向左移动飞船
            self.ship.move_left = True
        elif event.key == pygame.K_UP:
            # 向上移动飞船
            self.ship.move_up = True
        elif event.key == pygame.K_DOWN:
            # 向下移动飞船
            self.ship.move_down = True
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_event(self, event):
        """响应松开"""
        # 停止移动
        if event.key == pygame.K_SPACE:
            # 停止开火
            self._fire_stop_bullet()
        elif event.key == pygame.K_RIGHT:
            self.ship.move_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.move_left = False
        elif event.key == pygame.K_UP:
            self.ship.move_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.move_down = False

    def _fire_stop_bullet(self):
        """停止开火，并且将限制初始化"""
        self.setting.fire_bullet = False
        self.setting.fire_bullet_limit = self.setting.fire_bullet_limit_keep

    def _update_bullets(self):
        """创建子弹，并限制子弹数量和发射间隔，更新子弹位置并删除看不见的子弹"""
        # 创建子弹，并加以限制
        if len(self.bullets) < self.setting.bullet_allowed and self.setting.fire_bullet:
            if self.setting.fire_bullet_limit == self.setting.fire_bullet_limit_keep:
                self._fire_bullet()
                self.setting.fire_bullet_limit = 0
            else:
                self.setting.fire_bullet_limit += 1

        # 更新子弹位置
        self.bullets.update()

        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _fire_bullet(self):
        """创建一个子弹， 并将其加入到编组 bullets 中"""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)


if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
