import sys
import requests
from bs4 import BeautifulSoup
import WorkshopDL

#Find Submission Function
def UGCClassFinder(tag):
    return tag.has_attr("data-publishedfileid")

def scrape(SteamID64):
    #URL Setup
    BaseURL = "https://steamcommunity.com/profiles/"
    Endpoint = "/myworkshopfiles/?p="
    Page = 1
    SubmissionIDs = []
    #Get HTML
    while Page < 1668:
        EndpointRaw = requests.get(url = BaseURL + SteamID64 + Endpoint + str(Page))
        EndpointHTML = EndpointRaw.text
        #Parse HTML
        HTMLParse = BeautifulSoup(EndpointHTML, "html.parser")
        #find Submissions
        WorkshopSubmissions = HTMLParse.find_all(UGCClassFinder)
        for Submission in WorkshopSubmissions:
            SubmissionIDs.append(Submission.get("data-publishedfileid"))
        if len(WorkshopSubmissions) == 0:
            break
        Page += 1
    for SubmissionID in SubmissionIDs:
        WorkshopDL.download(SubmissionID)

if __name__ == '__main__':
    scrape(sys.argv[1])