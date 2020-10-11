import sys

import pygame

from setting import Setting

from ship import Ship

from bullet import BulletXNegative, BulletXPositive, BulletYPositive

from alien import Alien


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
        self.all_bullets = [pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()]
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def run_game(self):
        """开始游戏得主循环"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
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
        if len(self.all_bullets[0]) < self.setting.bullet_allowed and self.setting.fire_bullet:
            if self.setting.fire_bullet_limit == self.setting.fire_bullet_limit_keep:
                self._fire_bullet()
                self.setting.fire_bullet_limit = 0
            else:
                self.setting.fire_bullet_limit += 1

        # 更新子弹位置
        for value in range(0, 3):
            self.all_bullets[value].update()

        # 删除消失的子弹
        for bullets in self.all_bullets.copy():
            for bullet in bullets:
                if bullet.kinds == 0:
                    if bullet.rect.bottom <= 0:
                        self.all_bullets[bullet.kinds].remove(bullet)
                elif bullet.kinds == 1:
                    if bullet.rect.right <= 0:
                        self.all_bullets[bullet.kinds].remove(bullet)
                elif bullet.kinds == 2:
                    if bullet.rect.left >= self.ship.screen_rect.right:
                        self.all_bullets[bullet.kinds].remove(bullet)

    def _fire_bullet(self):
        """创建一个子弹， 并将其加入到编组 bullets 中"""
        new_bullet = BulletXPositive(self)
        self.all_bullets[2].add(new_bullet)
        new_bullet = BulletXNegative(self)
        self.all_bullets[1].add(new_bullet)
        new_bullet = BulletYPositive(self)
        self.all_bullets[0].add(new_bullet)

    def _create_fleet(self):
        """创建外星人飞船群"""
        # 创建一个外星人并计算一行可容纳多少个外星人。
        # 外星人的间距为外星人宽度
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.setting.screen_width - 4 * alien_width
        number_alien_x = available_space_x // (2 * alien_width)

        # 计算屏幕可容纳多少行外星人
        ship_height = self.ship.rect.height
        available_space_y = (self.setting.screen_height - ship_height -
                             (3 * alien_height))
        number_rows = available_space_y // (2 * alien_height)

        # 创建外星人群
        for row_number in range(number_rows):
            for alien_number in range(number_alien_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """创建一个外星人并将其放在相应的位置"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width * 2 + 2 * alien_number * alien_width
        alien.rect.x = alien.x
        alien.rect.y = alien_height + (2 * alien_height) * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        """
        检查是否有外星人位于屏幕边缘，
        并更新整群外星人位置
        """
        self._check_fleet_edges()
        self.aliens.update()

    def _check_fleet_edges(self):
        """有外星人到达边缘时采取相应措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整群外星人向下移，并改变他们额方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.setting.alien_fleet_drop_speed
        self.setting.fleet_direction *= -1

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        # 每次循环都会重绘屏幕
        self.screen.fill(self.setting.bg_color)
        self.ship.blitme()
        for value in range(0, 3):
            for bullet in self.all_bullets[value].sprites():
                bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # 让最近绘制得屏幕可见
        pygame.display.flip()


if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
