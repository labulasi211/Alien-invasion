import sys
from time import sleep
from random import randint

import pygame

from setting import Setting
from ship import Ship
from bullet import BulletXNegative, BulletXPositive, BulletYPositive
from alien import Alien
from game_stats import GameStats
from button import Button


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

        # 创立一个用于储存用于统计信息的实例
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.all_bullets = [pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()]
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # 创建 Play 按钮
        self.play_button = Button(self, "Play")

    def run_game(self):
        """开始游戏得主循环"""
        while True:
            self._check_events()

            if self.stats.game_active:
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_play_button(pygame.mouse.get_pos())

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
        elif event.key == pygame.K_p and not self.stats.game_active:
            self._restats_game()

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

    def _check_play_button(self, mouse_pos=(0, 0)):
        """在玩家单机 Play 按钮时，开启游戏"""
        if self.play_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            self._restats_game()

    def _restats_game(self):
        """重新开始游戏"""
        # 重置游戏的统计信息
        self.stats.game_active = True
        self.stats.reset_stats()

        # 开始新的一局
        self._replace_ship_and_aliens()

        # 隐藏鼠标光标
        pygame.mouse.set_visible(False)

        # 重置游戏设置
        self.setting.initialize_dynamic_setting()

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

        # 删除消失的所有子弹
        for bullets in self.all_bullets.copy():
            for bullet in bullets:
                self._delete_bullets(bullet)

        self._check_bullet_alien_collisions()

    def _delete_bullets(self, bullet):
        """删除到达边界的子弹"""
        if bullet.kinds == 0:
            if bullet.rect.bottom <= 0:
                self.all_bullets[bullet.kinds].remove(bullet)
        elif bullet.kinds == 1:
            if bullet.rect.right <= 0:
                self.all_bullets[bullet.kinds].remove(bullet)
        elif bullet.kinds == 2:
            if bullet.rect.left >= self.ship.screen_rect.right:
                self.all_bullets[bullet.kinds].remove(bullet)

    def _delete_all_bullets(self):
        """清除所有的子弹"""
        for value in range(3):
            self.all_bullets[value].empty()

    def _check_bullet_alien_collisions(self):
        """相应子弹核外星人碰撞"""
        # 检测是否有子弹击中外星人
        # 如果是的话，就删除相应的子弹和外星人，并将这些相对应的子弹和外星人
        # 通过键-值的形式保存起来
        for value in range(3):
            collisions = pygame.sprite.groupcollide(self.all_bullets[value], self.aliens, True, True)

        if not self.aliens:
            # 删除现在的所有子弹
            self._delete_all_bullets()
            self._create_fleet()
            self.setting.increase_speed()

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

        # 创建外星人群的数量
        alien_num = number_rows * number_alien_x // 2

        # 随机创建外星人群
        for value in range(alien_num):
            self._create_alien(available_space_x, available_space_y)

    def _create_alien(self, available_space_x, available_space_y):
        """创建一个外星人并将其放在相应的位置"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # 将外星人随机放在一个合适的区域中的某一个位置
        alien.x = randint(alien_width * 2, alien_width * 2 + available_space_x)
        alien.rect.x = alien.x

        # 让外星人的随机位置置于屏幕上方之外，让他们随机的进入屏幕
        alien.y = randint(-available_space_y, 0)
        alien.rect.y = alien.y
        alien.alien_speed = randint(
            self.setting.aliens_lowest_speed_x, self.setting.aliens_highest_speed_x
        ) * 0.1
        alien.alien_drop_speed = randint(
            self.setting.aliens_lowest_speed_y, self.setting.aliens_highest_speed_y
        ) * 0.01
        if randint(0, 1):
            alien.alien_direction = 1
        else:
            alien.alien_direction = -1
        self.aliens.add(alien)

    def _update_aliens(self):
        """
        检查是否有外星人位于屏幕边缘，
        并更新整群外星人位置
        """
        self._check_fleet_edges()
        self.aliens.update()

        # 检测外星人与飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 检测是否有外星人到达了屏幕底部
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """有外星人到达边缘时采取相应措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction(alien)

    def _change_fleet_direction(self, alien):
        """将整群外星人向下移，并改变他们额方向"""
        alien.alien_direction *= -1

    def _check_aliens_bottom(self):
        """检测是否有外星人到达了屏幕底端"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _ship_hit(self):
        """响应飞船被外星人撞到"""
        if self.stats.ships_left > 0:
            # 将 ship_left 减一
            self.stats.ships_left -= 1

            # 重新开始一局
            self._replace_ship_and_aliens()

            # 暂停
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _replace_ship_and_aliens(self):
        """重置外星人和飞船"""
        # 清空其余的外星人和子弹
        self._delete_all_bullets()
        self.aliens.empty()

        # 创建一群新的外星人，并将飞船放置到屏幕下方的中央
        self._create_fleet()
        self.ship.center_ship()

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        # 每次循环都会重绘屏幕
        self.screen.fill(self.setting.bg_color)
        self.ship.blitme()
        for value in range(0, 3):
            for bullet in self.all_bullets[value].sprites():
                bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # 如果游戏处于非活动状态，就绘制 Play 按钮
        if not self.stats.game_active:
            self.play_button.draw_button()

        # 让最近绘制得屏幕可见
        pygame.display.flip()


if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
