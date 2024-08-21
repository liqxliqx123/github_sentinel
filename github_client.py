import requests

class UpdateFetcher:
    def __init__(self, config):
        self.config = config
        self.headers = {"Authorization": f"token {self.config['github_token']}"}
        self.fetched_data = {}

    def fetch_issues(self, repo):
        response = requests.get(f"https://api.github.com/repos/{repo}/issues", headers=self.headers)
        return response.json()

    def fetch_pull_requests(self, repo):
        response = requests.get(f"https://api.github.com/repos/{repo}/pulls", headers=self.headers)
        return response.json()

    def fetch_all(self):
        for repo in self.config['subscriptions']:
            issues = self.fetch_issues(repo)
            pull_requests = self.fetch_pull_requests(repo)
            self.fetched_data[repo] = {
                "issues": issues,
                "pull_requests": pull_requests
            }

    def get_fetched_data(self):
        return self.fetched_data
