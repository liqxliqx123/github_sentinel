import requests

class UpdateFetcher:
    def __init__(self, config):
        self.config = config

    def fetch_updates(self):
        updates = {}
        for repo in self.config['subscriptions']:
            response = requests.get(f"https://api.github.com/repos/{repo}/events")
            if response.status_code == 200:
                updates[repo] = response.json()
        return updates
