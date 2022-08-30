import json
import os
import sys
import time

import requests

import WorkshopDL


def download(CollectionID, AppID=-1):
    """Downloads the metadata for a collection and then batch downloads the items in it"""
    # SteamWebAPI endpoint
    GetCollectionDetails = (
        "https://api.steampowered.com/ISteamRemoteStorage/GetCollectionDetails/v1/"
    )

    # Timeout Variable
    LoadAttempts = 1000

    # Load SteamWebAPI Key
    with open("./SteamWebAPI.key") as KeyFile:
        Key = KeyFile.read()

    # Load Workshop Page Details
    for _ in range(LoadAttempts):
        try:
            GetCollectionDetailsData = {
                "key": Key,
                "collectioncount": 1,
                "publishedfileids[0]": CollectionID,
            }
            GetCollectionDetailsRaw = requests.post(
                url=GetCollectionDetails, data=GetCollectionDetailsData
            )
            CollectionDetails = json.loads(GetCollectionDetailsRaw.text)["response"][
                "collectiondetails"
            ][0]
        except json.JSONDecodeError:
            time.sleep(3600)
            continue
        break
    WorkshopDL.download(CollectionID, True)
    if AppID != -1:
        os.makedirs("./" + str(AppID) + "/CollectionDetails/", exist_ok=True)
        with open(
            "./" + str(AppID) + "/CollectionDetails/" + str(CollectionID) + ".json", "w"
        ) as OutputFile:
            json.dump(CollectionDetails, OutputFile, sort_keys=True, indent=4)
    for Entry in CollectionDetails["children"]:
        WorkshopDL.download(Entry["publishedfileid"])


if __name__ == "__main__":
    download(sys.argv[1])
