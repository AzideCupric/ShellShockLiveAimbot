import logging
import logging.handlers

logger = logging.getLogger('ShellShock')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s")

f_handler = logging.FileHandler('shellshock.log')
f_handler.setFormatter(formatter)

s_handler = logging.StreamHandler()
s_handler.setFormatter(formatter)

logger.addHandler(f_handler)
logger.addHandler(s_handler)
