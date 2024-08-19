import os

import requests


class UpdateFetcher:
    def __init__(self, config):
        self.config = config

    def fetch_updates(self):
        updates = {}
        token = self.config['github_token']
        if not token:
            token = os.getenv("GITHUB_TOKEN")
        if not token:
            raise Exception(
                "No GitHub token found. Please set the GITHUB_TOKEN environment variable or provide it in the config file.")
        headers = {"Authorization": f"token {token}"}
        for repo in self.config['subscriptions']:
            response = requests.get(f"https://api.github.com/repos/{repo}/events", headers=headers)
            if response.status_code == 200:
                updates[repo] = response.json()
            else:
                print(f"Failed to fetch updates for {repo}: {response.status_code}")
        return updates
