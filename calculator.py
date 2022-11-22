import math
from .logger import logger

class Tank:
    name:str
    x:int
    y:int

    def __init__(self, name) -> None:
        self.name = name

class Shot:
    power:int
    angle:int

class gameEnv:
    g:float = -379.106
    q:float = 0.0518718
    z:float = 0.5
    wind:int = 0
    player:Tank
    enemy:Tank
    flatshot:Shot
    highshot:Shot

    def get_distance(self) -> tuple[int,int]:
        diffX = abs(self.enemy.x - self.player.x)
        diffY = self.player.y - self.enemy.y

        return (diffX, diffY)

    def get_power(self, angle:float) -> float:
        θ = math.radians(angle)
        cosθ = math.cos(θ)
        tanθ = math.tan(θ)
        x,y = self.get_distance()
        v_square = (-self.g * x * x) / (2* cosθ * cosθ * (tanθ * x - y))
        power = -2 / (self.g * self.q) * math.sqrt(v_square) 
        return power

    def get_power_with_wind(self, angle:float) -> float:
        θ = math.radians(angle)
        cosθ = math.cos(θ)
        sinθ = math.sin(θ)
        x,y = self.get_distance()
        w = self.z * self.wind
        denominator_square = 2 * self.g * cosθ * (x * sinθ + y * cosθ) + 2 * w * sinθ * (x * sinθ + y * cosθ)
        v = (self.g * x - w * y) / math.sqrt(denominator_square)
        power = -2 / (self.g * self.q) * v
        return power

    def get_flatshot(self) -> Shot:
        flat_power = 100
        flat_angle = 0

        for possible_angle in range(0, 90):
            try:
                if self.wind == 0:
                    power = self.get_power(possible_angle)
                else:
                    power = self.get_power_with_wind(possible_angle)
            except Exception:
                pass
            else:
                if power < flat_power:
                    flat_power = power
                    flat_angle = possible_angle
        
        logger.info("平射角度：%d\n平射力度：%2f", flat_angle, flat_power)
        flatshot = Shot(flat_angle, flat_power)
        self.flatshot = flatshot
        return flatshot

    def get_highshot(self) -> Shot:
        high_power = 101
        high_angle = -1

        for possible_angle in range(0, 90):
            try:
                if self.wind == 0:
                    power = self.get_power(90 - possible_angle)
                else:
                    power = self.get_power_with_wind(90 - possible_angle)
            except Exception:
                power = 101
            else:
                if power < 101:
                    high_angle = possible_angle
                    high_power = power
                    break
        
        logger.info("高射角度：%d\n高射力度：%2f", high_angle, high_power)
        highshot = Shot(high_angle, high_power)
        self.highshot = highshot
        return highshot
    
    