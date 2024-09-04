from config import Config
from init import Initializer
from utils.logger import LogManager

if __name__ == "__main__":
    config = Config().config
    LogManager()
    Initializer().command_run()
