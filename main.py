from src.config import Config
from src.init import run
from utils.logger import LogManager

if __name__ == "__main__":
    config = Config.load()
    LogManager()
    run()
