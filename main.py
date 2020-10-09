import json
import gspread
from gspread.models import Cell
import os
import time
import sys
import subprocess
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open("PlaylistBackup").sheet1 #which already shared google sheet to access 

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

def write_backup(videos):
    i = 2
    cells = []
    for video in videos:
        try:
            #LAST = sheet.cell(1, 2).value
            #sheet.update_cell(1, 1, video)
            cells.append(Cell(i, 1, video))
            print(video)
            i+=1
        except:
            print('**FAILED** to load data from sheets,sad')
            time.sleep(10)
            sys.exit(0)
    sheet.update_cells(cells)

def read_backup():
    backup = [item for item in sheet.col_values(1) if item]
    return backup

def cross_check(backup,videos):
    i = 0
    for item in backup:
        print(item,videos[i])
        if item == "BACKUP":
            print('first line, ignoring')
            pass
        elif item in videos[i]:
            i+=1
        else:
            i+=1
            if sheet.cell(i+1, 2).value == "":
                sheet.update_cell(i+1, 2, f"We got bamboozled, backup was: {item}")

if __name__ == '__main__':
    videos = fetch_all_youtube_videos("PLO6X7bUkuOMu4VIHjmjVoPlMEGf7ULwxC")
    backup = read_backup()
    cross_check(backup,videos)
    #write_backup(videos)