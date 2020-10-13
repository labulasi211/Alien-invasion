import pygame.font


class Scoreboard:
    """显示得分信息"""

    def __init__(self, ai_game):
        """初始化显示得分涉及的属性"""
        self.ships_image = []
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.setting = ai_game.setting
        self.stats = ai_game.stats

        # 加载飞船图像，用于显示剩余的飞船数
        for value in range(3):
            self.ships_image.append([pygame.image.load('images/ship.png')])
            self.ships_image[value].append(self.ships_image[value][0].get_rect())


        # 显示得分信息时使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 30)
        # 设置初始得分图像和游戏等级
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ship()

    def prep_score(self):
        """将得分信息转换为一副渲染的图像"""
        round_score = round(self.stats.score, -1)
        score_str = "{:,}".format(round_score)
        self.score_image = self.font.render("score: " + score_str, True, self.text_color)

        # 在屏幕右上角显示得分
        self.score_image_rect = self.score_image.get_rect()
        self.score_image_rect.right = self.screen_rect.right - 10
        self.score_image_rect.top = 10

    def prep_high_score(self):
        """将最高得分转化为一副渲染图像"""
        round_high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(round_high_score)
        self.high_score_image = self.font.render("high score: " + high_score_str, True, self.text_color)

        # 将最高得分显示在屏幕顶部中央
        self.high_score_image_rect = self.high_score_image.get_rect()
        self.high_score_image_rect.centerx = self.screen_rect.centerx
        self.high_score_image_rect.top = self.screen_rect.top

    def prep_level(self):
        """将游戏等级转换为一副渲染图像"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render("level: " + level_str, True, self.text_color)

        # 将游戏等级显示在游戏得分下面
        self.level_image_rect = self.level_image.get_rect()
        self.level_image_rect.right = self.score_image_rect.right
        self.level_image_rect.top = self.score_image_rect.bottom + 5

    def prep_ship(self):
        """将飞船的剩余数量显示在屏幕的左上角"""
        for number_ship in range(self.stats.ships_left):
            self.ships_image[number_ship][1].left = (
                    number_ship * self.ships_image[number_ship][1].width + 5
            )
            self.ships_image[number_ship][1].top = 5

    def show_score(self):
        """在屏幕上显示得分和游戏等级"""
        self.screen.blit(self.score_image, self.score_image_rect)
        self.screen.blit(self.high_score_image, self.high_score_image_rect)
        self.screen.blit(self.level_image, self.level_image_rect)
        for number_ship in range(self.stats.ships_left):
            self.screen.blit(self.ships_image[number_ship][0], self.ships_image[number_ship][1])