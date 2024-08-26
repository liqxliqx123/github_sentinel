import io
import os

from src.config import Config
from src.exporter import Exporter
from src.github_client import UpdateFetcher
from src.llm import LLMModule
from utils import logger
from utils.logger import LogManager


class ReportGenerator:
    def __init__(self):
        self.llm_module = LLMModule()
        config = Config.get_config()
        self.report_dir_name = config["report_dir_name"]
        if self.report_dir_name:
            os.makedirs(self.report_dir_name, exist_ok=True)
        self.logger = LogManager.get_logger()

    def generate_daily_report(self, filepath):
        self.logger.debug(filepath)
        with open(filepath, 'r') as md_file:
            content = md_file.read()

        summary = self.llm_module.generate_daily_report(content)
        if not summary:
            return
        report_dir_name = os.path.dirname(os.path.dirname(filepath))

        report_filename = filepath.replace(report_dir_name, self.report_dir_name)
        report_filename = report_filename.replace(".md", "_report.md")
        repo_name = os.path.dirname(report_filename)
        os.makedirs(repo_name, exist_ok=True)
        with open(report_filename, 'w') as report_file:
            report_file.write(summary)

        return report_filename

    def get_report_content(self, repo: str) -> (str, str, str, str):
        # TODO: get report content from report file
        report_issue_file_path = ""
        report_pr_file_path = ""
        # fetch
        self.logger.debug("Fetching updates for all subscribed repositories...")
        update_fetcher = UpdateFetcher()
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
            return "", "", report_issue_file_path, report_pr_file_path

        # generate report
        markdown_issue_files = []
        markdown_pr_files = []
        for repo, data in updates.items():
            issue_files, pr_files = exporter.export_all(repo, data['issues'], data['pull_requests'])
            markdown_issue_files.append(issue_files)
            markdown_pr_files.append(pr_files)

        # 创建一个string buffer
        report_issue_buffer = io.StringIO()
        report_pr_buffer = io.StringIO()
        report_issue_file_paths = []
        report_pr_file_paths = []
        # generate issue report
        for file in markdown_issue_files:
            report_file_name = self.generate_daily_report(file)
            with open(report_file_name, "r") as f:
                report_issue_buffer.write(f.read())
                report_issue_file_paths.append(report_file_name)
        # generate pr report
        for file in markdown_pr_files:
            report_file_name = self.generate_daily_report(file)
            with open(report_file_name, "r") as f:
                report_pr_buffer.write(f.read())
                report_pr_file_paths.append(report_file_name)

        self.logger.debug("Reports generated successfully.")
        report_issue_content = report_issue_buffer.getvalue()
        report_pr_content = report_pr_buffer.getvalue()
        report_issue_buffer.close()
        report_pr_buffer.close()
        if len(report_issue_file_paths) > 0:
            report_issue_file_path = report_issue_file_paths[0]
        if len(report_pr_file_paths) > 0:
            report_pr_file_path = report_pr_file_paths[0]
        return report_issue_content, report_pr_content, report_issue_file_path, report_pr_file_path
