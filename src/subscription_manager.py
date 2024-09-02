from config import Config


class SubscriptionManager:
    def __init__(self):
        self.config = Config().config
        self.subscriptions = self.config['subscriptions']

    def get_subscriptions(self):
        address = []
        for _, v in self.subscriptions.items():
            for addr in v:
                address.append(addr)
        return address
