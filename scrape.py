import json
import requests
import pprint
from bs4 import BeautifulSoup
from sys import argv

key = ''
workshopID = 68540175

endpoint = "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"
data = {'key':key,'itemcount':1,'publishedfileids[0]':workshopID}

r = requests.post(url = endpoint, data = data)
jsondata = r.json()

filename = jsondata['response']['publishedfiledetails'][0]['filename']

print(filename)