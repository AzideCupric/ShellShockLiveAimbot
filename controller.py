from typing import Literal
from pynput import keyboard, mouse
import time
import platform

from .logger import logger
from .calculator import gameEnv

class Bot:
    env:gameEnv
    keys:keyboard.Controller
    mouse:mouse.Controller
    reset_power:int = 100
    reset_angle:int = 90

    def controller_reset(self) -> None:
        """炮管复位到垂直角度:angle=90,power=100"""
        player = self.env.player
        self.mouse.position = (player.x, player.y)
        time.sleep(0.05)
        mouse.press(mouse.Button.left)
        time.sleep(0.05)
        mouse.move(0,-player.y)
        time.sleep(0.05)
        mouse.release(mouse.Button.left)
        logger.info("炮管复位至angle：90，power：100")

    def get_enemy_direction(self) -> Literal["left", "right"]:
        if self.env.player.x < self.env.enemy.x:
            logger.info("检测到敌方在我方左侧")
            return "right"
        else:
            logger.info("检测到敌方在我方右侧")
            return "left"

    def set_power_and_angle_by_mode(self, mode:Literal["flat","high"]) -> None:
        self.controller_reset()
        mode_name = "平射" if mode == "flat" else "高射"
        match mode:
            case "flat":
                diff_power = self.env.flatshot.power - self.reset_power
                diff_angle = self.env.flatshot.angle - self.reset_angle
            case "high":
                diff_power = self.env.highshot.power - self.reset_power
                diff_angle = self.env.highshot.power - self.reset_angle
        
        if diff_power > 0:
            for _ in range(0, diff_power):
                self.keys.tap(keyboard.Key.up)
                time.sleep(0.05)
        else:
            for _ in range(0, diff_power):
                self.keys.tap(keyboard.Key.down)
                time.sleep(0.05)
        logger.info("%s发射力度设置完成", mode_name)

        if diff_angle > 0:
            for _ in range(0, diff_angle):
                self.keys.tap(keyboard.Key.right)
                time.sleep(0.05)
        else:
            for _ in range(0, diff_angle):
                self.keys.tap(keyboard.Key.left)
                time.sleep(0.05)
        logger.info("%s发射角度调整完成", mode_name)

    def get_player_pos(self, x:int, y:int, _, pressed:bool):
        if pressed:
            logger.info("设定当前玩家位置为：%d, %d", x, y)
            self.env.player.x = x
            self.env.player.y = y
            return False #return False 表示关闭监听
        return True
    
    def locate_player(self):
        logger.info("使用鼠标点击玩家坦克位置：")
        mouse_listener = mouse.Listener(on_click=self.get_player_pos)
        mouse_listener.start()
        mouse_listener.join()
    
    def get_enemy_pos(self, x:int, y:int, _, pressed:bool):
        if pressed:
            logger.info("设定当前敌方位置为：%d, %d", x, y)
            self.env.enemy.x = x
            self.env.enemy.y = y
            return False # 参见get_player_pos()
        return True
    
    def locate_enemy(self):
        logger.info("使用鼠标点击敌方坦克位置")
        mouse_listener = mouse.Listener(on_click=self.get_enemy_pos)
        mouse_listener.start()
        mouse_listener.join()
        
    def get_wind_num(self, key):
        if platform.system() == "Linux":
            if key == keyboard.Key.enter:
                logger.info("设置风力为%s", wind_str)
                
                return False
            if hasattr(key, 'char'):
                if key.char is None:
                    wind_str = "5"
                elif key.char in "1234567890":
                    wind_str += key.char
        