import gradio as gr

from src.config import Config
from src.init import Initializer
from src.report_generator import ReportGenerator
from src.subscription_manager import SubscriptionManager
from utils.logger import LogManager


def process_input(selected_option, value):
    # 根据下拉框选择和滑块值生成Markdown内容
    issue_content, pr_content, issue_filepath, pr_filepath = ReportGenerator().get_report_content(
        selected_option)

    return issue_content, pr_content, issue_filepath, pr_filepath


def main():
    # 创建Gradio界面
    with gr.Blocks() as demo:
        # 下拉框，提供选项供选择
        scribe = SubscriptionManager()
        choices = scribe.get_subscriptions()
        dropdown = gr.Dropdown(choices=choices, label="选择订阅的repo")

        # 滑块
        slider = gr.Slider(minimum=1, maximum=7, step=1, label="最近几天")

        # 输出Markdown展示
        # 将报告预览部分分为左右两栏
        with gr.Row():
            with gr.Column():
                # 左侧报告预览
                gr.Label("issue")
                markdown_output_issue = gr.Markdown(label="报告预览(issue)")
                issue_link = gr.File(label="下载报告")
            with gr.Column():
                # 右侧报告预览
                gr.Label("pull-request")
                markdown_output_pull_request = gr.Markdown(label="报告预览(pull request)")
                pr_link = gr.File(label="下载报告")

        # 按钮，触发处理
        submit_button = gr.Button("提交")

        # 绑定函数到按钮点击事件
        submit_button.click(process_input, inputs=[dropdown, slider],
                            outputs=[markdown_output_issue, markdown_output_pull_request, issue_link, pr_link])
    return demo


if __name__ == "__main__":
    config = Config.load()
    LogManager()
    Initializer()
    main().queue().launch(share=False, debug=True)
