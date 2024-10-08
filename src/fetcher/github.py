from datetime import datetime, timedelta
from utils.logger import LogManager

import requests
from config import Config


class GithubFetcher:
    def __init__(self, data_range=1, since=None, until=None):
        self.until = None
        self.since = None
        self.config = Config().config
        self.headers = {"Authorization": f"token {self.config['github_token']}"}
        self.fetched_data = {}
        self.get_data_range(data_range)
        self.logger = LogManager().logger

    def get_data_range(self, data_range: int):
        if 0 < data_range < 7:
            self.since = (datetime.now() - timedelta(days=data_range)).strftime("%Y-%m-%dT00:00:00Z")
            self.until = None
        else:
            raise ValueError("Data range must be between 1 and 7 days")

    def fetch_issues(self, repo):
        since = self.since
        until = self.until
        params = {"state": "closed"}
        if not self.since:
            since = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        params["since"] = since
        response = requests.get(f"https://api.github.com/repos/{repo}/issues", headers=self.headers,
                                params=params)
        if response.status_code == 200:
            issues = response.json()
            if self.until:
                until_time = datetime.strptime(until, "%Y-%m-%dT%H:%M:%SZ")
            else:
                until_time = datetime.now()
            return [
                issue for issue in issues
                if datetime.strptime(issue["created_at"], "%Y-%m-%dT%H:%M:%SZ") <= until_time
            ]
        else:
            self.logger.error(f"get {repo} issues error, {response.status_code}: {response.text}")
            return []

    def fetch_pull_requests(self, repo):
        since = self.since
        until = self.until
        response = requests.get(f"https://api.github.com/repos/{repo}/pulls", headers=self.headers,
                                params={"state": "closed"})
        if response.status_code == 200:
            prs = response.json()

            if not since:
                since = datetime.now().strftime("%Y-%m-%dT00:00:00Z")
            since_time = datetime.strptime(since, "%Y-%m-%dT%H:%M:%SZ")
            if not until:
                until_time = datetime.now()
            else:
                until_time = datetime.strptime(self.until, "%Y-%m-%dT%H:%M:%SZ")
            return [
                pr for pr in prs
                if datetime.strptime(pr["created_at"], "%Y-%m-%dT%H:%M:%SZ") >= since_time and datetime.strptime(
                    pr["created_at"], "%Y-%m-%dT%H:%M:%SZ") <= until_time
            ]
        else:
            self.logger.error(f"get {repo} issues error,{response.status_code}: {response.text}")
            return []

    def fetch_data(self, repo):
        issues = self.fetch_issues(repo)
        pull_requests = self.fetch_pull_requests(repo)
        self.fetched_data[repo] = {
            "issues": issues,
            "pull_requests": pull_requests
        }

    def fetch_all(self):
        for _, topic in self.config['subscriptions'].items():
            for repo in topic:
                issues = self.fetch_issues(repo)
                pull_requests = self.fetch_pull_requests(repo)
                self.fetched_data[repo] = {
                    "issues": issues,
                    "pull_requests": pull_requests
                }

    def get_fetched_data(self):
        return self.fetched_data
