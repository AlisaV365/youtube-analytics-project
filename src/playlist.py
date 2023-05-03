import os, datetime, isodate

from googleapiclient.discovery import build


from dotenv import load_dotenv

load_dotenv()


class PlayList:
    api_key = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id: str) -> None:
        self.playlist = self.youtube.playlists().list(part="snippet,contentDetails", id=playlist_id).execute()
        # название плэйлиста
        self.title = self.playlist['items'][0]['snippet']['title']
        # ссылка на плэйлист
        self.url = "https://www.youtube.com/playlist?list=" + playlist_id
        # данные по видеороликам в плейлисте
        self.playlist_videos = self.youtube.playlistItems().list(
            playlistId=playlist_id,
            part='contentDetails',
            maxResults=50,
        ).execute()
        # все id видеороликов из плейлиста
        self.video_id: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        # информация о видеороликах из плейлиста по их id
        self.video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                         id=','.join(self.video_id)
                                                         ).execute()

    @property
    # возвращает объект класса `datetime.timedelta` с суммарной длительность плейлиста
    def total_duration(self):
        total_time_videos = datetime.timedelta()
        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_time_videos += duration
        return total_time_videos

    # возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
    def show_best_video(self):
        like_count = 0
        for video in self.video_response['items']:
            video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                        id=video['id']).execute()
            if int(video_response['items'][0]['statistics']['likeCount']) > like_count:
                like_count = int(video_response['items'][0]['statistics']['likeCount'])
                self.video_url = video_response['items'][0]['id']

        return f'https://youtu.be/{self.video_url}'

