import requests
import datetime
import json
from zipfile import ZipFile
import os
import sys
from os.path import basename

# google oauth2 refresh token
refresh_token = ""

zipObj = ZipFile('backup.zip', 'w')

args = sys.argv[1:]

for arg in args:
    for folderName, subfolders, filenames in os.walk(arg):
        for filename in filenames:
            #create complete filepath of file in directory
            filePath = os.path.join(folderName, filename)
            print(filePath)
            # add file to zip but maintain folder structure
            zipObj.write(filePath, filePath)
            
zipObj.close()

# write a request to refresh to google oauth2 token and save it to a variable
r = requests.post("https://oauth2.googleapis.com/token", data={
    "client_id": "<Google Cloud Platform Client ID>",
    "client_secret": "<Google Cloud Platform Client Secret>",
    "refresh_token": refresh_token,
    "grant_type": "refresh_token"
})

# get the access token from the response
access_token = r.json()["access_token"]

# get current date and time
now = datetime.datetime.now()

# use the access token to make a request to the google drive api to upload a local file called "backup.zip" and save it as "backup.zip" on google drive
r = requests.post("https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart", headers={
    "Authorization": f"Bearer {access_token}",
}, files={
    'data': ('metadata', json.dumps({"name": f"backup-{now.now()}.zip", "parents": ["<Google Drive Folder ID To Upload To>"]}), 'application/json; charset=UTF-8'),
    "file": ("application/zip", open("backup.zip", "rb"))
})

print(r.json())

os.remove("backup.zip")