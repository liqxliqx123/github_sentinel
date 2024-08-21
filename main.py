import threading
from config import Config
from subscription_manager import SubscriptionManager
from github_client import UpdateFetcher
from notifier import Notifier
from report_generator import ReportGenerator
from scheduler import Scheduler
from command_handler import handle_command, print_help
from exporter import Exporter
from llm import LLMModule


def run_scheduler(scheduler):
    scheduler.start()


def main():
    config = Config.load()

    subscription_manager = SubscriptionManager(config)
    update_fetcher = UpdateFetcher(config)
    exporter = Exporter(config)
    notifier = Notifier(config)
    llm_module = LLMModule()
    report_generator = ReportGenerator(llm_module, config)
    scheduler = Scheduler(config, update_fetcher, notifier, report_generator)

    # Print help message on startup
    print_help()

    # Run Scheduler in background
    threading.Thread(target=run_scheduler, args=(scheduler,)).start()

    # Start command loop for interactive input
    handle_command(subscription_manager, update_fetcher, scheduler, report_generator, exporter)


if __name__ == "__main__":
    main()
