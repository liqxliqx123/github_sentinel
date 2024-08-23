from config import Config


class Notifier:
    def __init__(self):
        self.config = Config.get_config()

    def send_notification(self, message):
        # 示例：发送邮件通知
        print(f"Sending notification: {message}")
