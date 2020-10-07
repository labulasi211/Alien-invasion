import sys

import pygame

class AlienInvasion:
    """管理游戏资源和行为得类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()

        self.screen = pygame.display.set_mode(1200, 800)
        pygame.display.set_caption("Alien Invasion")

    def run_game(self):
        """开始游戏得主循环"""
        while True:
            # 监视键盘和鼠标得事件
            for even in pygame.event.get():
                if even.type == pygame.QUIT:
                    sys.exit()

            # 让最近绘制得屏幕可见
            pygame.display.flip()


if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()