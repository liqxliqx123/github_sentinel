class Notifier:
    def __init__(self, config):
        self.config = config

    def send_notification(self, message):
        # 示例：发送邮件通知
        print(f"Sending notification: {message}")
