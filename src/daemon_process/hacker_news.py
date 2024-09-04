import datetime
import os

from config import Config
from fetcher.hacker_news import fetch_hackernews_top_stories
from report_generator import ReportGenerator
from utils.logger import LogManager
from utils.path import get_daily_export_path

from utils.path import get_daily_report_path


class DaemonHackerNews:
    def __init__(self):
        self.config = Config().config
        self.freq_hours = self.config['daemon']['hacker_news']['freq_hours']
        self.freq_days = self.config['daemon']['hacker_news']['freq_days']

    def hacker_news_hours_job(self):
        logger = LogManager().logger
        logger.info(f"begin hacker news job every {self.freq_hours} hours ...")
        stories = fetch_hackernews_top_stories()
        summary = ReportGenerator().generate_hacker_news_report(stories)
        if summary:
            time_now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            file_path = os.path.join(get_daily_export_path(), f'hacker_news_report_{time_now}.md')
            ReportGenerator().export_report(summary, file_path)
        else:
            logger.info("no hacker news stories to report")

    def hacker_news_daily_report_job(self):
        logger = LogManager().logger
        logger.info(f"begin hacker news job every {self.freq_days} days ...")
        summary = ReportGenerator().generate_hacker_news_daily_report()
        if summary:
            time_now = datetime.datetime.now().strftime('%Y%m%d')
            file_path = os.path.join(get_daily_report_path(), f'hacker_news_daily_report_{time_now}.md')
            ReportGenerator().export_report(summary, file_path)
        else:
            logger.info("no daily hacker news stories to report")