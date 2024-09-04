import sys
from pathlib import Path

current_file_path = Path(__file__).resolve()
project_root = current_file_path.parent.parent
sys.path.insert(0, str(project_root))

import time
import schedule
from daemon_process.hacker_news import DaemonHackerNews
from daemon_process.github import DaemonGithub
from config import Config


class DaemonJobs:
    def __init__(self):
        self.config = Config().config

    def run_hacker_news_hours_job(self, at: str):
        job = DaemonHackerNews().hacker_news_hours_job
        # 首先运行一次, 如果不需要请注释
        # job()
        schedule.every().days.at(at).do(job)

    def run_hacker_news_daily_report_job(self, at: str = "08:00"):
        job = DaemonHackerNews().hacker_news_daily_report_job
        # 首先运行一次, 如果不需要请注释
        # job()
        schedule.every().days.at(at).do(job)

    def run_github_job(self, at: str = "07:30"):
        freq_days = self.config["daemon"]["github"]["freq_days"]
        execution_time = self.config["daemon"]["github"]["execution_time"]
        if at != "":
            execution_time = at
        job = DaemonGithub().github_job
        # 首先运行一次, 如果不需要请注释
        job(freq_days)
        schedule.every(freq_days).day.at(execution_time).do(job, freq_days)


def main():
    # hacker news
    jobs = DaemonJobs()
    jobs.run_hacker_news_hours_job("07:00")
    jobs.run_hacker_news_hours_job("15:00")
    jobs.run_hacker_news_hours_job("23:00")
    jobs.run_hacker_news_daily_report_job()
    # github
    jobs.run_github_job("15:48")
    while True:
        schedule.run_pending()  # 检查是否有任务需要执行
        time.sleep(1)  # 等待1秒


if __name__ == '__main__':
    main()
