import json
import requests
from bs4 import BeautifulSoup
from sys import argv

jsondata = ''

key = 'A1A81C10144C6843539A230EDF00DCBC'

endpoint = "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"
data = {'key':key,'itemcount':1,'publishedfileids[0]':68540175}

r = requests.post(url = endpoint, data = data)
jsondata = r.json

print(jsondata)