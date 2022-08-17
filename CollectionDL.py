import json
import requests
import WorkshopDL
import sys
import time


def download(CollectionID):
    """Downloads the metadata for a collection and then batch downloads the items in it"""
    # SteamWebAPI endpoint
    GetCollectionDetails = "https://api.steampowered.com/ISteamRemoteStorage/GetCollectionDetails/v1/"

    # Timeout Variable
    LoadAttempts = 1000

    # Load SteamWebAPI Key
    with open("./SteamWebAPI.key", "r") as KeyFile:
        Key = KeyFile.read()

    # Load Workshop Page Details
    for _ in range(LoadAttempts):
        try:
            GetCollectionDetailsData = {"key": Key, "collectioncount": 1, "publishedfileids[0]": CollectionID}
            GetCollectionDetailsRaw = requests.post(url=GetCollectionDetails, data=GetCollectionDetailsData)
            CollectionDetails = json.loads(GetCollectionDetailsRaw.text)["response"]["collectiondetails"][0]
        except json.JSONDecodeError:
            time.sleep(3600)
            continue
        break
    WorkshopDL.download(CollectionID, True)
    for Entry in CollectionDetails["children"]:
        WorkshopDL.download(Entry["publishedfileid"])


if __name__ == "__main__":
    download(sys.argv[1])
