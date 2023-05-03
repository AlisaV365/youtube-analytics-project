import json
import os
from googleapiclient.discovery import build

from dotenv import load_dotenv

load_dotenv()

YT_API_KEY = os.getenv('YT_API_KEY')


class Channel:
    """Класс для ютуб-канала"""
    api_key = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = Channel.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = 'https:////www.youtube.com//channel//' + self.channel['items'][0]['id']
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.view_count = self.channel['items'][0]['statistics']['viewCount']

    def __add__(self, other):
        if type(other) == Channel:
            return int(self.subscriber_count) + int(other.subscriber_count)
        else:
            raise TypeError

    def __str__(self):  # функция возвращает строку, содержащую название и URL
        return f"{self.title} ({self.url})"

    def __sub__(self, other):  # преобразование количества подписчиков из строки в целое число затем  вычитание
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __lt__(self, other):  # метод для операции сравнения «больше»
        return self.subscriber_count > other.subscriber_count

    def __le__(self, other):  # данный метод проверяет, что количество подписчиков больше или равно
        return self.subscriber_count >= other.subscriber_count

    def __eq__(self, other):  # сравнения двух объектов класса
        return self.subscriber_count == other.subscriber_count

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return cls.youtube

    def to_json(self, file_name):
        with open(file_name, 'w', encoding='cp1251') as fh:
            json.dump({
                'channel_id': self.__channel_id,
                'title': self.title,
                'description': self.description,
                'url': self.url,
                'subscriber_count': self.subscriber_count,
                'video_count': self.video_count,
                'view_count': self.view_count
            }, fh)
