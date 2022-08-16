import json
import sys
import datetime
import requests
import os

GetPublishedFileDetails = "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"
KeyFile = open("./SteamWebAPI.key", "r")
Key = KeyFile.read()
KeyFile.close()

WorkshopID = str(sys.argv[1])
RequestData = {'key':Key,'itemcount':1,'publishedfileids[0]':WorkshopID}
GetPublishedFileDetailsRaw = requests.post(url = GetPublishedFileDetails, data = RequestData)
PublishedFileDetails = json.loads(GetPublishedFileDetailsRaw.text)['response']['publishedfiledetails'][0]

print(json.dumps(PublishedFileDetails, sort_keys=True, indent=4))