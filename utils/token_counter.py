import tiktoken

from src.config import Config


class TokenCounter:
    def __init__(self):
        conf = Config.get_config()
        self.model = conf["model_name"]
        self.encoding = tiktoken.encoding_for_model(self.model)

    def count_tokens(self, text: str) -> int:
        tokens = self.encoding.encode(text)
        return len(tokens)

    def count_message_tokens(self, messages: list) -> int:
        """
        计算多条消息中的 token 数量.
        参数:
        - messages: 包含消息内容的列表，每条消息是一个字典，至少包含 'role' 和 'content' 键.
        示例:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Tell me a joke."},
            {"role": "assistant", "content": "Why did the chicken cross the road? To get to the other side!"}
        ]
        """
        tokens_per_message = 4  # 每条消息的固定开销
        tokens_per_name = -1  # 如果消息中包含 'name' 键

        total_tokens = 0
        for message in messages:
            total_tokens += tokens_per_message  # 消息开销
            total_tokens += len(self.encoding.encode(message["content"]))  # 消息内容 token 数量
            total_tokens += len(self.encoding.encode(message.get("name", "")))  # 消息名称 token 数量

        return total_tokens


# 使用示例
if __name__ == "__main__":
    token_counter = TokenCounter(model="gpt-4")

    # 单个文本的 token 计数
    text = "Hello, how are you?"
    print(f"Token count for text: {token_counter.count_tokens(text)}")

    # 多条消息的 token 计数
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Tell me a joke."},
        {"role": "assistant", "content": "Why did the chicken cross the road? To get to the other side!"}
    ]
    print(f"Token count for messages: {token_counter.count_message_tokens(messages)}")
