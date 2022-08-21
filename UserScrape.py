import sys
import requests
from bs4 import BeautifulSoup
import WorkshopDL
import CollectionDL
from tqdm.auto import trange



def UGCClassFinder(tag):
    """BeautifulSoup filter that finds HTML tags with a data-publishedfileid attribute"""
    return tag.has_attr("data-publishedfileid")


def scrape(SteamID64):
    """Batch download the Steam Workshop submissions of a user with the specific SteamID64"""
    # URL Setup
    BaseURL = "https://steamcommunity.com/profiles/"
    Endpoint = "/myworkshopfiles/?p="
    EndpointCollections = "/myworkshopfiles/?section=collections&p="
    SubmissionIDs = []
    CollectionIDs = []
    # Get HTML
    for Page in trange(1668, desc="Retrieving Item Pages"):
        EndpointRaw = requests.get(url=BaseURL + SteamID64 + Endpoint + str(Page + 1))
        EndpointHTML = EndpointRaw.text
        # Parse HTML
        HTMLParse = BeautifulSoup(EndpointHTML, "html.parser")
        # find Submissions
        WorkshopSubmissions = HTMLParse.find_all(UGCClassFinder)
        for Submission in WorkshopSubmissions:
            SubmissionIDs.append(Submission.get("data-publishedfileid"))
        if len(WorkshopSubmissions) == 0:
            break
    for SubmissionID in SubmissionIDs:
        WorkshopDL.download(SubmissionID)

    for Page2 in trange(1668, desc="Retrieving Collection Pages"):
        EndpointCollectionsRaw = requests.get(url=BaseURL + SteamID64 + EndpointCollections + str(Page2 + 1))
        EndpointCollectionsHTML = EndpointCollectionsRaw.text
        # Parse HTML
        HTMLParse = BeautifulSoup(EndpointCollectionsHTML, "html.parser")
        # find Submissions
        WorkshopCollections = HTMLParse.find_all(UGCClassFinder)
        for Collection in WorkshopCollections:
            CollectionIDs.append(Collection.get("data-publishedfileid"))
        if len(WorkshopCollections) == 0:
            break
    for CollectionID in CollectionIDs:
        CollectionDL.download(CollectionID)

if __name__ == "__main__":
    scrape(sys.argv[1])
