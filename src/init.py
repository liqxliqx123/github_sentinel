import threading

from subscription_manager import SubscriptionManager
from fetcher.github import GithubFetcher
from notifier import Notifier
from report_generator import ReportGenerator
from command_handler import handle_command, print_help
from exporter import Exporter
from llm.gpt4 import GPT4Module


class Initializer:
    def __init__(self):
        self.subscription_manager = SubscriptionManager()
        self.update_fetcher = GithubFetcher()
        self.exporter = Exporter()
        self.notifier = Notifier()
        self.llm_module = GPT4Module()
        self.report_generator = ReportGenerator()

    def command_run(self):
        # Print help message on startup
        print_help()

        # Start command loop for interactive input
        handle_command(self.subscription_manager, self.update_fetcher, self.report_generator,
                       self.exporter)
