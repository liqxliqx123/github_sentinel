import os
from datetime import datetime

from config import Config
from utils.path import get_daily_export_path


class Exporter:
    def __init__(self):
        self.config = Config().config
        self.date_str = datetime.now().strftime('%Y-%m-%d')

    def export_to_markdown(self, repo, issues, pull_requests):

        filename = f"{self.date_str}_report.md"
        repo_path = os.path.join(get_daily_export_path(), repo.replace('/', '_'))
        filepath = os.path.join(repo_path, filename)

        os.makedirs(repo_path, exist_ok=True)

        with open(filepath, 'w') as md_file:
            # write issue
            md_file.write(f"# Issues for {repo} on {self.date_str}\n\n")

            for issue in issues:
                md_file.write(
                    f"- [{issue['title']}]({issue['html_url']}) by {issue['user']['login']} at {issue['created_at']}\n")
            # write pr
            md_file.write(f"\n\n# Pull Requests for {repo} on {self.date_str}\n\n")

            for pr in pull_requests:
                md_file.write(f"- [{pr['title']}]({pr['html_url']}) by {pr['user']['login']} at {pr['created_at']}\n")

        return filepath

    def export_pull_requests_to_markdown(self, repo, pull_requests):

        filename = f"{self.date_str}_prs.md"
        repo_path = os.path.join(self.base_path, repo.replace('/', '_'))
        filepath = os.path.join(repo_path, filename)

        os.makedirs(repo_path, exist_ok=True)

        with open(filepath, 'w') as md_file:
            md_file.write(f"# Pull Requests for {repo} on {self.date_str}\n\n")

            for pr in pull_requests:
                md_file.write(f"- [{pr['title']}]({pr['html_url']}) by {pr['user']['login']} at {pr['created_at']}\n")

        return filepath

    def export_all(self, repo, issues, pull_requests):
        return self.export_to_markdown(repo, issues, pull_requests)
