import json
import sys
import datetime
import requests

GetPublishedFileDetails = "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"
key_file = open("./SteamWebAPI.key", "r")
key = key_file.read()
key_file.close()

print(key)