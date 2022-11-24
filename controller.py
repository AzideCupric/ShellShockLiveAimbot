from typing import Literal
from pynput import keyboard, mouse
import time

from .logger import logger
from .calculator import gameEnv

class Bot:
    env:gameEnv
    wind_str:str = ""
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
        
        def key_adjust(end, press_key, wait_time = 0.05):
            for _ in range(0, end):
                self.keys.tap(press_key)
                time.sleep(wait_time)
        
        if diff_power > 0:
            key_adjust(diff_power, keyboard.Key.up)
        else:
            key_adjust(diff_power, keyboard.Key.down)
        logger.info("%s发射力度设置完成", mode_name)

        if diff_angle > 0:
            key_adjust(diff_angle, keyboard.Key.right)    
        else:
            key_adjust(diff_power, keyboard.Key.left)
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
        if key == keyboard.Key.enter:
            logger.info("读取完成，风力大小：%s", self.wind_str)
            self.env.wind = ord(self.wind_str)
            return False
        
        if key == keyboard.Key.backspace:
            self.wind_str = self.wind_str[:len(self.wind_str) - 1]
        elif hasattr(key,'char') and key.char in '1234567890':
            self.wind_str += key.char
        
        logger.info("当前总输入为：%s", self.wind_str)
        
    def set_wind(self):
        with keyboard.Listener(on_press=self.get_wind_num) as lst:
            lst.join()
        