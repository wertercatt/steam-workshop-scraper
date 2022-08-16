import sys
import os
import requests
from bs4 import BeautifulSoup
import json

#URL Setup
BaseURL = "https://steamcommunity.com/profiles/"
SteamID64 = str(sys.argv[1])
Endpoint = "/myworkshopfiles/?p="

EndpointRaw = requests.get(url = BaseURL + SteamID64 + Endpoint + str(1))
EndpointHTML = EndpointRaw.text

HTMLParse = BeautifulSoup(EndpointHTML, 'html.parser')

WorkshopSubmissions = HTMLParse.find("class", id="ugc")
print(json.dumps(WorkshopSubmissions, sort_keys=True, indent=4))