class ReportGenerator:
    def __init__(self, config):
        self.config = config

    def generate_report(self, updates):
        report = "Daily/Weekly Update Report\n"
        for repo, events in updates.items():
            report += f"\nRepository: {repo}\n"
            for event in events:
                report += f" - {event['type']}: {event['created_at']}\n"
        return report
