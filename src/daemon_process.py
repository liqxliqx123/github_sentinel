import schedule
import time

from config import Config
from notifier import Notifier
from utils.logger import LogManager
from fetcher.hacker_news import fetch_hackernews_top_stories
from report_generator import ReportGenerator


def github_job(timedelta: int):
    logger = LogManager().logger
    logger.info("begin github job...")
    subscribed_repos = Config().config["subscriptions"]["github"]
    for repo in subscribed_repos:
        logger.info(f"begin to generate report for {repo}")
        report_content, _ = ReportGenerator().get_report_content(
            repo, timedelta)
        logger.info(f"end to generate report for {repo}")
        Notifier().notify(f"[GitHubSentinel]{repo} 进展简报", report_content)


def run_github_job():
    config = Config().config
    freq_days = config["schedule"]["github"]["freq_days"]
    execution_time = config["schedule"]["github"]["execution_time"]
    github_job(freq_days)
    schedule.every(freq_days).day.at(execution_time).do(github_job)


def hacker_news_job():
    logger = LogManager().logger
    logger.info("begin hacker news job...")
    stories = fetch_hackernews_top_stories()
    summary = ReportGenerator().generate_hacker_news_report(stories)
    if summary:
        Notifier().notify("[GitHubSentinel] hacker_news 进展简报", summary)


def run_hacker_news_job():
    config = Config().config
    freq_days = config["schedule"]["hacker_news"]["freq_days"]
    execution_time = config["schedule"]["hacker_news"]["execution_time"]
    hacker_news_job()
    schedule.every(freq_days).day.at(execution_time).do(hacker_news_job)


# for test
def test_mail():
    print("test mail...")


# for test
def run_test_mail():
    github_job(1)
    schedule.every().minute.at(":16").do(github_job, 1)


def main():
    run_github_job()
    run_hacker_news_job()
    # run_test_mail()
    while True:
        schedule.run_pending()  # 检查是否有任务需要执行
        time.sleep(1)  # 等待1秒


if __name__ == '__main__':
    main()
