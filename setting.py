class Setting:
    """储存游戏《外星人入侵》中所有设置得类"""

    def __init__(self):
        """初始化游戏设置"""
        # 屏幕设置
        self.screen_width = 900
        self.screen_height = 600
        self.bg_color = (230, 230, 230)

        # 飞船设置
        self.ship_speed = 1.5
        self.ship_limit = 3

        # 子弹设置
        self.bullet_color = (60, 60, 60)
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_speed = 3
        self.bullet_allowed = 3
        # 开火标识符
        self.fire_bullet = False
        # 开火频率限度
        self.fire_bullet_limit_keep = 50
        self.fire_bullet_limit = self.fire_bullet_limit_keep  # 用于计数限制长按空格时子弹发射速度

        # 外星人设置
        self.alien_speed = 1.0
        self.alien_fleet_drop_speed = 10
        # fleet_direction 为1表示外星人向右移，为-1表示外星人向左移
        self.fleet_direction = 1



