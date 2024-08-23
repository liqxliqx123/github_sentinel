import threading

from src.subscription_manager import SubscriptionManager
from src.github_client import UpdateFetcher
from src.notifier import Notifier
from src.report_generator import ReportGenerator
from src.scheduler import Scheduler
from src.command_handler import handle_command, print_help
from src.exporter import Exporter
from src.llm import LLMModule
from utils.token_counter import TokenCounter


def run_scheduler(scheduler):
    scheduler.start()


def run():
    subscription_manager = SubscriptionManager()
    update_fetcher = UpdateFetcher()
    exporter = Exporter()
    notifier = Notifier()
    llm_module = LLMModule()
    report_generator = ReportGenerator(llm_module)
    scheduler = Scheduler(update_fetcher, notifier, report_generator)

    # Print help message on startup
    print_help()

    # Run Scheduler in background
    threading.Thread(target=run_scheduler, args=(scheduler,)).start()

    # Start command loop for interactive input
    handle_command(subscription_manager, update_fetcher, scheduler, report_generator, exporter)
