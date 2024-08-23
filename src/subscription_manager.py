from src.config import Config


class SubscriptionManager:
    def __init__(self):
        self.config = Config.get_config()
        self.subscriptions = self.config['subscriptions']

    def add_subscription(self, repo):
        if repo not in self.subscriptions:
            self.subscriptions.append(repo)
            self.save_subscriptions()

    def remove_subscription(self, repo):
        if repo in self.subscriptions:
            self.subscriptions.remove(repo)
            self.save_subscriptions()

    def save_subscriptions(self):
        self.config['subscriptions'] = self.subscriptions
        Config.save(self.config)
