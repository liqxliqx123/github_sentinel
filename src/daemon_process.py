import schedule
import time

from src.config import Config
from src.notifier import Notifier
from src.report_generator import ReportGenerator
from src.utils.logger import LogManager


def github_job(timedelta: int):
    logger = LogManager().logger
    logger.info("begin github job...")
    subscribed_repos = Config().config["subscriptions"]["github"]
    for repo in subscribed_repos:
        logger.info(f"begin to generate report for {repo}")
        issue_content, pr_content, _, _ = ReportGenerator().get_report_content(
            repo, timedelta)
        logger.info(f"end to generate report for {repo}")
        content = f"{issue_content}\n\n{pr_content}"
        Notifier().notify(repo, content)


def run_github_job():
    config = Config().config
    freq_days = config["schedule"]["github"]["freq_days"]
    execution_time = config["schedule"]["github"]["execution_time"]
    github_job(freq_days)
    schedule.every(freq_days).day().at(execution_time).do(github_job)


# for test
def test_mail():
    print("test mail...")


# for test
def run_test_mail():
    github_job(1)
    schedule.every().minute.at(":16").do(github_job, 1)


def main():
    run_github_job()
    # run_test_mail()
    while True:
        schedule.run_pending()  # 检查是否有任务需要执行
        time.sleep(1)  # 等待1秒


if __name__ == '__main__':
    main()
