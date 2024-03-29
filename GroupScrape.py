import sys

import requests
from bs4 import BeautifulSoup

import UserScrape


def scrape(GroupName):
    """Batch downloads the submissions of all users in a given Steam group"""
    BaseURL = "https://steamcommunity.com/groups/"
    Endpoint = "/memberslistxml/?xml=1"
    EndpointRaw = requests.get(url=BaseURL + GroupName + Endpoint)
    EndpointXML = EndpointRaw.text
    XMLParse = BeautifulSoup(EndpointXML, "xml")
    SteamID64s = XMLParse.find_all("steamID64")
    for SteamID64 in SteamID64s:
        UserScrape.scrape(SteamID64.get_text())


if __name__ == "__main__":
    scrape(sys.argv[1])
