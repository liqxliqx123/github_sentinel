from config import Config
from subscription_manager import SubscriptionManager
from update_fetcher import UpdateFetcher
from notifier import Notifier
from report_generator import ReportGenerator
from scheduler import Scheduler

def main():
    config = Config.load()

    subscription_manager = SubscriptionManager(config)
    update_fetcher = UpdateFetcher(config)
    notifier = Notifier(config)
    report_generator = ReportGenerator(config)
    scheduler = Scheduler(config)

    scheduler.run(update_fetcher, notifier, report_generator)

if __name__ == "__main__":
    main()
