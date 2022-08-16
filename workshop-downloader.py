import json
import sys
import datetime
import requests
import os

GetPublishedFileDetails = "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"
GetCollectionDetails = "https://api.steampowered.com/ISteamRemoteStorage/GetCollectionDetails/v1/"
GetUGCFileDetails = "https://api.steampowered.com/ISteamRemoteStorage/GetUGCFileDetails/v1/"
KeyFile = open("./SteamWebAPI.key", "r")
Key = KeyFile.read()
KeyFile.close()

WorkshopID = str(sys.argv[1])
GetPublishedFileDetailsData = {"key":Key,"itemcount":1,"publishedfileids[0]":WorkshopID}
GetPublishedFileDetailsRaw = requests.post(url = GetPublishedFileDetails, data = GetPublishedFileDetailsData)
PublishedFileDetails = json.loads(GetPublishedFileDetailsRaw.text)["response"]["publishedfiledetails"][0]

print(json.dumps(PublishedFileDetails, sort_keys=True, indent=4))

AppID = PublishedFileDetails["consumer_app_id"]
SteamID64 = PublishedFileDetails["creator"]
DateCreated = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc) + datetime.timedelta(seconds=PublishedFileDetails["time_created"])
DateCreatedISO8601 = DateCreated.strftime("%Y-%m-%dT%H-%M-%S")

print(DateCreatedISO8601)