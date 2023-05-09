import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from dotenv import load_dotenv

load_dotenv()

YT_API_KEY = os.getenv('YT_API_KEY')


class Video:
    api_key = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str):
        self.video_id = video_id

        try:
            self.video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                             id=self.video_id).execute()
            self.title = self.video_response['items'][0]['snippet']['title']
            self.url = f"https://www.youtube.com/watch?v={self.video_id}"
            self.view_count = self.video_response['items'][0]['statistics']['viewCount']
            self.like_count = self.video_response['items'][0]['statistics']['likeCount']
        except:
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None

        # except HttpError as error:
        #     if error.video_response == 404:
        #         print(f"Видео {self.video_id} не найдено")

    # возваращает название видео
    def __str__(self):
        return self.title


class PLVideo(Video):
    # наследование с переопределением
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

    # возваращает название видео
    def __str__(self):
        return self.title
