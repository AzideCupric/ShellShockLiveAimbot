from typing import Literal
from pynput import keyboard, mouse
import time

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

        if diff_power > 0:
            for _ in range(0, diff_power):
                self.keys.tap(keyboard.Key.up)
                time.sleep(0.05)
            logger.info("%s炮管上抬完成", mode_name)
        else:
            for _ in range(0, diff_power):
                self.keys.tap(keyboard.Key.down)
                time.sleep(0.05)
            logger.info("%s炮管下抬完成", mode_name)

        