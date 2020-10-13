class Setting:
    """储存游戏《外星人入侵》中所有设置得类"""

    def __init__(self):
        """初始化游戏设置"""
        # 屏幕设置
        self.screen_width = 900
        self.screen_height = 600
        self.bg_color = (230, 230, 230)

        # 飞船设置
        self.ship_limit = 3

        # 子弹设置
        self.bullet_color = (60, 60, 60)
        self.bullet_width = 30
        self.bullet_height = 15
        self.bullet_allowed = 10
        # 开火标识符
        self.fire_bullet = False
        # 开火频率限度
        self.fire_bullet_limit_keep = 50
        self.fire_bullet_limit = self.fire_bullet_limit_keep  # 用于计数限制长按空格时子弹发射速度

        # 加快游戏节奏的速度
        self.ship_speedup_scale = 1.1
        self.bullet_speedup_scale = 1.1
        self.aliens_speedup_scale_x = 1
        self.aliens_speedup_scale_y = 3

        self.initialize_dynamic_setting()

    def initialize_dynamic_setting(self):
        """初始化随游戏经行而变化的数据"""
        self.bullet_speed = 3.0
        self.ship_speed = 1.5
        self.aliens_lowest_speed_x = 1
        self.aliens_lowest_speed_y = 5
        self.aliens_highest_speed_x = 5
        self.aliens_highest_speed_y = 20

    def increase_speed(self):
        """提升速度设置"""
        self.aliens_lowest_speed_y += self.aliens_speedup_scale_y
        self.aliens_lowest_speed_x += self.aliens_speedup_scale_x
        self.aliens_highest_speed_x += self.aliens_speedup_scale_x
        self.aliens_highest_speed_y += self.aliens_speedup_scale_y
        self.ship_speed *= self.ship_speedup_scale
        self.bullet_speed *= self.bullet_speedup_scale





