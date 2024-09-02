import gradio as gr

from config import Config
from init import Initializer
from report_generator import ReportGenerator
from subscription_manager import SubscriptionManager
from utils.logger import LogManager


def process_input(selected_option, value):
    # 根据下拉框选择和滑块值生成Markdown内容
    return ReportGenerator().get_report_content(
        selected_option, value)


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
        with gr.Row():
            with gr.Column():
                # 左侧报告预览
                gr.Label("报告预览")
                preview = gr.Markdown(label="报告预览")
                file_link = gr.File(label="下载报告")

        # 按钮，触发处理
        submit_button = gr.Button("提交")

        # 绑定函数到按钮点击事件
        submit_button.click(process_input, inputs=[dropdown, slider],
                            outputs=[preview, file_link])
    return demo


if __name__ == "__main__":
    config = Config().config
    LogManager()
    Initializer()
    main().queue().launch(share=False, debug=True)
