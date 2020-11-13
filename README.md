# Youtube Playlist Backup
Automatically backup each entry on a youtube playlist.

Videos found on playlists on Youtube are often made private or deleted, that leads to user confusion since they no longer can access the title of the deleted video.  
Since I have big playlists on youtube and I hate it when something like that happens I made this basic script to backup the title of every entry on a playlist while also checking for deleted videos and documenting them (while keeping the backed up title).  

# INSTRUCTIONS
1.Install dependencies  
2.Create a file named creds.json and populate the values with the following structure  
`
{
    "YT_API_KEY": "your youtube api key here",
    "PLAYLISTS":{
        "playlist1": "your playlist id here",
        "playlist2": "your playlist id here"} 
}
`  
3.Get your Youtube api key from Google APIs  
4.Get your Google Drive client_secret.json from Google APIs  
5.Share your target document with the email address found on your client_secret.json under "client_email"  

