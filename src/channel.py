import json
import os
from googleapiclient.discovery import build

from dotenv import load_dotenv

load_dotenv()

YT_API_KEY = os.getenv('YT_API_KEY')


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str):
        self.__channel_id: str = channel_id  # id канала
        response = self.get_info()
        self.__title: str = response['items'][0]['snippet']['title']  # название канала
        self.__description: str = response['items'][0]['snippet']['description']  # описание канала
        self.__url: str = 'https://www.youtube.com/channel/' + channel_id  # ссылка на канал
        self.__subscribers: int = int(response['items'][0]['statistics']['subscriberCount'])  # количество подписчиков
        self.__video_count: int = int(response['items'][0]['statistics']['videoCount'])  # количество видео
        self.__view_count: int = int(response['items'][0]['statistics']['viewCount'])  # общее количество просмотров


    @classmethod
    def get_service(cls):  # возвращает объект для работы с YouTube API
        return build('youtube', 'v3', developerKey=YT_API_KEY)

    def to_json(self, filename): # преобразование данных в формат json
        data = {
            "channel_id": self.channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscribers_count": self.subscriber_count,
            "video_count": self.video_count,
            "view_count": self.view_count
        }

        with open(filename, 'w') as file:
            data = json.dumps(data)
            file.write(data)


    def get_info(self) -> dict:  # получает информацию о канале
        response = self.get_service().channels().list(
            id=self.channel_id,
            part='snippet,statistics'
        ).execute()
        return response

    def print_info(self):  # выводит на экран информацию о канале
        response = self.get_info()
        print(json.dumps(response, indent=2, ensure_ascii=False))

