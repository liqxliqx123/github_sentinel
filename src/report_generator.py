import glob
import io
import os
from datetime import datetime, timedelta

from exporter import Exporter
from fetcher.github import GithubFetcher
from llm.llm import LLM
from utils.path import get_daily_report_path, get_daily_export_path
from utils.logger import LogManager


class ReportGenerator:
    def __init__(self):
        self.llm = LLM()
        self.logger = LogManager().logger

    def generate_daily_report(self, filepath):
        self.logger.debug(f"读取本地文件: {filepath}")
        with open(filepath, 'r') as md_file:
            content = md_file.read()

        summary = self.llm.model.generate_report("github", content)
        if not summary:
            return
        report_dir_name = os.path.dirname(os.path.dirname(filepath))
        report_filename = filepath.replace(report_dir_name, get_daily_report_path())
        repo_name = os.path.dirname(report_filename)
        os.makedirs(repo_name, exist_ok=True)
        with open(report_filename, 'w') as report_file:
            report_file.write(summary)

        return report_filename

    def get_report_content(self, repo: str, time_delta: int) -> (str, str):
        # TODO: get report content from report file
        report_content = ""
        report_path = ""
        # fetch
        self.logger.debug("Fetching updates for all subscribed repositories...")
        update_fetcher = GithubFetcher(data_range=time_delta)
        update_fetcher.fetch_data(repo)
        self.logger.debug("Updates fetched successfully.")

        # export
        updates = update_fetcher.get_fetched_data()
        exporter = Exporter()
        if updates:
            for repo, data in updates.items():
                exporter.export_all(repo, data['issues'], data['pull_requests'])
            self.logger.debug("Updates exported to Markdown files.")
        else:
            self.logger.debug("No updates to export. Please fetch updates first.")
            return report_content, report_path
        # generate report
        markdown_files = []
        for repo, data in updates.items():
            report_files = exporter.export_all(repo, data['issues'], data['pull_requests'])
            markdown_files.append(report_files)

        # 创建一个string buffer
        report_buffer = io.StringIO()
        report_file_paths = []
        for file in markdown_files:
            report_file_name = self.generate_daily_report(file)
            with open(report_file_name, "r") as f:
                report_buffer.write(f.read())
                report_file_paths.append(report_file_name)

        self.logger.debug("Reports generated successfully.")
        report_content = report_buffer.getvalue()
        report_buffer.close()
        if len(report_file_paths) > 0:
            report_path = report_file_paths[0]
        return report_content, report_path

    def generate_hacker_news_report(self, stories):
        summary = ""
        content = io.StringIO()
        for story in stories:
            content.write(f"{story['title']}\n{story['link']}\n\n")
        try:
            summary = self.llm.model.generate_report("hacker_news_hours", content.getvalue())
        except Exception as e:
            self.logger.error(f"Error generating hacker news report: {e}")
        content.close()
        return summary

    def generate_hacker_news_daily_report(self):
        summary = ""
        content = io.StringIO()
        # 找到export目录下前一天的hacker news文件
        previous_day_str = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
        for filename in glob.glob(
                os.path.join(get_daily_export_path(), f"hacker_news_report_{previous_day_str}_*.md")):
            with open(filename, "r") as f:
                hours_summary = f.read()
                content.write(hours_summary)
                content.write("\n\n")
        try:
            summary = self.llm.model.generate_report("hacker_news_daily_report", content.getvalue())
        except Exception as e:
            self.logger.error(f"Error generating hacker news report: {e}")
        content.close()
        return summary

    def export_report(self, content: str, filepath: str):
        dir_name = os.path.dirname(filepath)
        os.makedirs(dir_name, exist_ok=True)
        with open(filepath, 'w') as report_file:
            report_file.write(content)
        self.logger.debug(f"Report exported to {filepath}")
