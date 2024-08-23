import schedule
import time
import threading

from src.config import Config


class Scheduler:
    def __init__(self, update_fetcher, notifier, report_generator):
        self.config = Config.get_config()
        self.update_fetcher = update_fetcher
        self.notifier = notifier
        self.report_generator = report_generator
        self.scheduler_thread = threading.Thread(target=self.run)
        self.scheduler_thread.daemon = True

    def start(self):
        self.scheduler_thread.start()

    def run(self):
        schedule.every().day.at("09:00").do(self.job)

        while True:
            schedule.run_pending()
            time.sleep(1)

    def job(self):
        updates = self.update_fetcher.fetch_updates()
        report = self.report_generator.generate_report(updates)
        self.notifier.send_notification(report)
