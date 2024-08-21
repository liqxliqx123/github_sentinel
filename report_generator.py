import os


class ReportGenerator:
    def __init__(self, llm_module, config):
        self.llm_module = llm_module
        self.report_dir_name = config["report_dir_name"]
        if self.report_dir_name:
            os.makedirs(self.report_dir_name, exist_ok=True)

    def generate_daily_report(self, filepath):
        print(filepath)
        with open(filepath, 'r') as md_file:
            content = md_file.read()

        summary = self.llm_module.generate_daily_report(content)

        dir_name = os.path.dirname(filepath)
        report_filename = filepath.replace(dir_name, self.report_dir_name)
        report_filename = filepath.replace(".md", "_report.md")
        with open(report_filename, 'w') as report_file:
            report_file.write(summary)

        return report_filename
