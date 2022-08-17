import requests
from bs4 import BeautifulSoup
import UserScrape
import sys

def scrape(GroupName):
    BaseURL = "https://steamcommunity.com/groups/"
    Endpoint = "/memberslistxml/?xml=1"
    EndpointRaw = requests.get(url = BaseURL + GroupName + Endpoint)
    EndpointXML = EndpointRaw.text
    XMLParse = BeautifulSoup(EndpointXML, "xml")
    SteamID64s = XMLParse.find_all("steamID64")
    for SteamID64 in SteamID64s:
        UserScrape.scrape(SteamID64.get_text())
if __name__ == "__main__":
    scrape(sys.argv[1])
