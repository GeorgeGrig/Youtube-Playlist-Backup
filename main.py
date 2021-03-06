#INSTRUCTIONS
# 1.Install dependencies
# 2.Create a file named creds.json and populate the values with the following structure
#{
#    "YT_API_KEY": "your youtube api key here",
#    "PLAYLISTS":{
#        "playlist1": "your playlist id here",
#        "playlist2": "your playlist id here"} 
#}
# 3.Get your Youtube api key from Google APIs
# 4.Get your Google Drive client_secret.json from Google APIs
# 5.Share your target document with the email address found on your client_secret.json under "client_email"

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

#Get credentials and value init
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
 
with open("creds.json", "r") as read_file:
    data = json.load(read_file)


#Fetch all playlist entries using the youtube api
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
    #return a clean entry title list
    list = []
    for video in res["items"]:
        list.append(video.get('snippet')['title'])
    list.reverse()
    return list

#Write the new values to the sheet
def write_backup(videos):
    i = 2
    cells = []
    for video in videos:
        try:
            cells.append(Cell(i, 1, video))
            i+=1
        except:
            print('**FAILED**')
    sheet.update_cells(cells)

#Read backup values from the sheet
def read_backup():
    backup = [item for item in sheet.col_values(1) if item]
    return backup

#Check line by line if there are any changes and document them
def cross_check(backup,videos):
    i = 0
    names = sheet.col_values(1)
    checks = sheet.col_values(2)
    for item in backup:
        if item == "BACKUP":
            print('first line, ignoring')
        elif item in videos:
            i+=1
        elif item == "":
            i+=1
        elif checks == []:
            i+=1
            if names[i+2] != "":
                time.sleep(1.1)
                sheet.update_cell(i+1, 2, f"We got bamboozled, backup was '{item}' and new item is '{videos[i-1]}'")
        else:
            i+=1
            try:
                if checks[i+2] == "" and names[i+2] != "":
                    time.sleep(1.1)
                    sheet.update_cell(i+1, 2, f"We got bamboozled, backup was '{item}' and new item is '{videos[i-1]}'")
            except:
                if names[i+2] != "":
                    time.sleep(1.1)
                    sheet.update_cell(i+1, 2, f"We got bamboozled, backup was '{item}' and new item is '{videos[i-1]}'")

if __name__ == '__main__':
    playlists = data["PLAYLISTS"].values()
    i = 0
    for playlist in playlists:
        sheet = client.open("PlaylistBackup").get_worksheet(i) #which already shared google sheet to access
        videos = fetch_all_youtube_videos(playlist)
        backup = read_backup()
        cross_check(backup,videos)
        write_backup(videos)
        i += 1