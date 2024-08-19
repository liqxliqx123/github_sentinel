import schedule
import time

class Scheduler:
    def __init__(self, config):
        self.config = config

    def run(self, update_fetcher, notifier, report_generator):
        schedule.every().day.at("09:00").do(self.job, update_fetcher, notifier, report_generator)

        while True:
            schedule.run_pending()
            time.sleep(1)

    def job(self, update_fetcher, notifier, report_generator):
        updates = update_fetcher.fetch_updates()
        report = report_generator.generate_report(updates)
        notifier.send_notification(report)
