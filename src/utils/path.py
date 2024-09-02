import os


# 获取当前文件的绝对路径
def get_current_file_path():
    return os.path.abspath(__file__)


# 根据当前文件的路径获取 settings.json的路径
def get_settings_json_path():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(get_current_file_path()))), 'settings.json')


# 获取daily_export的路径
def get_daily_export_path():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(get_current_file_path()))), 'export')

def get_daily_report_path():
    report_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(get_current_file_path()))), 'report')
    if not os.path.exists(report_path):
        os.makedirs(report_path, exist_ok=True)
    return report_path


# 获取prompt的路径
def get_prompt_path():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(get_current_file_path()))), 'prompt')


def get_gpt_4o_mini_prompt_path():
    return os.path.join(get_prompt_path(), 'gpt_4o_mini')
