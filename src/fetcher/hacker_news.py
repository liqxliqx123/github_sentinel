import requests
from bs4 import BeautifulSoup

from config import Config
from utils.logger import LogManager


def fetch_hackernews_top_stories():
    logger = LogManager().logger
    logger.debug("开始爬取 Hacker News...")
    conf = Config().config
    url = conf['hacker_news']['url']
    response = requests.get(url, timeout=30)
    logger.debug(f"爬取完成, status code: {response.status_code}")
    response.raise_for_status()  # 检查请求是否成功

    soup = BeautifulSoup(response.text, 'html.parser')
    # 查找包含新闻的所有 <tr> 标签
    stories = soup.find_all('tr', class_='athing')

    top_stories = []
    for story in stories:
        title_tag = story.find('span', class_='titleline').find('a')
        if title_tag:
            title = title_tag.text
            link = title_tag['href']
            top_stories.append({'title': title, 'link': link})

    return top_stories


if __name__ == "__main__":
    stories = fetch_hackernews_top_stories()
    if stories:
        for idx, story in enumerate(stories, start=1):
            print(f"{idx}. {story['title']}")
            print(f"   Link: {story['link']}")
    else:
        print("No stories found.")
