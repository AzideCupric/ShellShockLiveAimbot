import logging
import logging.handlers

logger = logging.getLogger('ShellShock')
logger.setLevel(logging.DEBUG)

f_handler = logging.FileHandler('shellshock.log')
f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

logger.addHandler(f_handler)