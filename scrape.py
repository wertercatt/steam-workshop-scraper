import valve
import json
import requests
from bs4 import BeautifulSoup
from sys import argv

output = ''

valve.steam.api.interface.API.__init__(key=,format='json',versions=None, interfaces=ISteamRemoteStorage)

with valve.steam.api.interface.ISteamRemoteStorage as interface:

	output == interface.GetPublishedFileDetails(1,68540239)
	print(output)