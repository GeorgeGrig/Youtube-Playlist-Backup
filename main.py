from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json

with open("creds.json", "r") as read_file:
    data = json.load(read_file)

def fetch_all_youtube_videos(playlistId):
    youtube = build('youtube', 'v3', developerKey=data["YT_API_KEY"])
    res = youtube.playlistItems().list(
    part="snippet",
    playlistId=playlistId,
    maxResults="50"
    ).execute()

    nextPageToken = res.get('nextPageToken')
    while ('nextPageToken' in res):
        nextPage = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlistId,
        maxResults="50",
        pageToken=nextPageToken
        ).execute()
        res['items'] = res['items'] + nextPage['items']

        if 'nextPageToken' not in nextPage:
            res.pop('nextPageToken', None)
        else:
            nextPageToken = nextPage['nextPageToken']
    list = []
    for video in res["items"]:
        list.append(video.get('snippet')['title'])
    return list

if __name__ == '__main__':
    videos = fetch_all_youtube_videos("PLO6X7bUkuOMu4VIHjmjVoPlMEGf7ULwxC")
    print(videos)