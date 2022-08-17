import json
import requests
import WorkshopDL
import sys
import os

def download(CollectionID):
    """Downloads the metadata for a collection and then batch downloads the items in it (Not Implemented)"""
    # SteamWebAPI endpoint
    GetCollectionDetails = "https://api.steampowered.com/ISteamRemoteStorage/GetCollectionDetails/v1/"
    print(CollectionID)
    print(GetCollectionDetails)

if __name__ == "__main__":
    download(sys.argv[1])
