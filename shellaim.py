from controller import Bot
from calculator import Tank, gameEnv
from pynput import keyboard, mouse

player = Tank("player")
enemy = Tank("enemy")

env = gameEnv(player=player, enemy=enemy)

keys = keyboard.Controller()
ms = mouse.Controller()

aim_bot = Bot(env=env, keys=keys, mouse=ms)

hot_key_config:dict ={
    '<ctrl>+<shift>+P': aim_bot.locate_player, 
    '<ctrl>+<shift>+E': aim_bot.locate_enemy, 
    '<ctrl>+<shift>+F': aim_bot.prepare_flatshot, 
    '<ctrl>+<shift>+H': aim_bot.prepare_highshot, 
    '<ctrl>+<shift>+W': aim_bot.set_wind,
    '<ctrl>+<shift>+C': exit
}
if __name__ == "__main__":
    with keyboard.GlobalHotKeys(hot_key_config) as bot_listener:
        bot_listener.join()