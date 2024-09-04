import schedule
from utils.logger import LogManager

from config import Config

from report_generator import ReportGenerator

from notifier import Notifier


class DaemonGithub:
    def __init__(self):
        self.logger = LogManager().logger
        self.config = Config().config

    def github_job(self, timedelta: int = 1):
        self.logger.info("begin github job...")
        subscribed_repos = self.config["subscriptions"]["github"]
        for repo in subscribed_repos:
            self.logger.info(f"begin to generate report for {repo}")
            report_content, _ = ReportGenerator().get_report_content(
                repo, timedelta)
            self.logger.info(f"end to generate report for {repo}")
            Notifier().notify(f"[GitHubSentinel]{repo} 进展简报", report_content)
