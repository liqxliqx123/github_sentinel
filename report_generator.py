import os

from config import Config


class ReportGenerator:
    def __init__(self, llm_module):
        self.llm_module = llm_module
        config = Config.get_config()
        self.report_dir_name = config["report_dir_name"]
        if self.report_dir_name:
            os.makedirs(self.report_dir_name, exist_ok=True)

    def generate_daily_report(self, filepath):
        print(filepath)
        with open(filepath, 'r') as md_file:
            content = md_file.read()

        summary = self.llm_module.generate_daily_report(content)

        report_dir_name = os.path.dirname(os.path.dirname(filepath))

        report_filename = filepath.replace(report_dir_name, self.report_dir_name)
        report_filename = report_filename.replace(".md", "_report.md")
        with open(report_filename, 'w') as report_file:
            report_file.write(summary)

        return report_filename
