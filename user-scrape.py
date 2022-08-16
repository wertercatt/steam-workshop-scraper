import sys
import os
import requests
from bs4 import BeautifulSoup
import json

#Find Submission Function
def UGCClassFinder(tag):
    return tag.has_attr("data-publishedfileid")


#URL Setup
BaseURL = "https://steamcommunity.com/profiles/"
SteamID64 = str(sys.argv[1])
Endpoint = "/myworkshopfiles/?p="
Page = 1
#Get HTML
while Page < 1668:
    EndpointRaw = requests.get(url = BaseURL + SteamID64 + Endpoint + str(Page))
    EndpointHTML = EndpointRaw.text
    #Parse HTML
    HTMLParse = BeautifulSoup(EndpointHTML, "html.parser")
    #find Submissions
    WorkshopSubmissions = HTMLParse.find_all(UGCClassFinder)
    for Submission in WorkshopSubmissions:
        print(Submission.get("data-publishedfileid"))
    if len(WorkshopSubmissions) == 0:
        break
    Page += 1