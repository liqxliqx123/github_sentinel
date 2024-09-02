import threading

from src.subscription_manager import SubscriptionManager
from src.fetcher.github import GithubFetcher
from src.notifier import Notifier
from src.report_generator import ReportGenerator
from src.command_handler import handle_command, print_help
from src.exporter import Exporter
from src.llm.gpt4 import GPT4Module


class Initializer:
    def __init__(self):
        self.subscription_manager = SubscriptionManager()
        self.update_fetcher = GithubFetcher()
        self.exporter = Exporter()
        self.notifier = Notifier()
        self.llm_module = GPT4Module()
        self.report_generator = ReportGenerator()
        self.scheduler = Scheduler(self.update_fetcher, self.notifier, self.report_generator)
        self.scheduler.start()

    def run_scheduler(self, scheduler):
        scheduler.start()

    def command_run(self):
        # Print help message on startup
        print_help()
        # Run Scheduler in background
        threading.Thread(target=self.run_scheduler, args=(self.scheduler,)).start()

        # Start command loop for interactive input
        handle_command(self.subscription_manager, self.update_fetcher, self.scheduler, self.report_generator,
                       self.exporter)
