from loguru import logger
import os
import sys

from config import Config


class LogManager:
    _logger = None

    def __init__(self):
        conf = Config().config
        self.log_dir = conf["log"]["dir"]
        self.log_level = conf["log"]["level"].upper()
        if LogManager._logger is None:
            self._setup_logger()
        self.logger = LogManager._logger

    def _setup_logger(self):
        # 创建日志目录
        os.makedirs(self.log_dir, exist_ok=True)

        # 日志文件路径
        log_file = os.path.join(self.log_dir, "app.log")

        # 配置日志格式
        log_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{module}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        )

        # 清除默认的日志处理器
        logger.remove()

        # 添加新的日志处理器
        logger.add(sys.stdout, level=self.log_level, format=log_format)  # 控制台输出
        # logger.add(log_file, level=self.log_level, format=log_format, rotation="1 week", compression="zip")  # 文件输出

        # 可选：添加一个文件记录错误级别及以上的日志
        error_log_file = os.path.join(self.log_dir, "error.log")
        logger.add(error_log_file, level="ERROR", format=log_format, rotation="50 MB", compression="zip")

        LogManager._logger = logger


# 使用示例
if __name__ == "__main__":
    # LogManager(log_dir="../../logs", log_level="DEBUG")
    config = Config("../settings.json").config
    logger = LogManager(config).logger

    logger.info("This is an info message.")
    logger.debug("This is a debug message.")
    logger.error("This is an error message.")
