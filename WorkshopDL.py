import json
import sys
import datetime
import requests
import os
from pathvalidate import sanitize_filepath
import time
from tqdm.auto import trange



def download(WorkshopID, IsCollection=False):
    """Downloads the given WorkshopID"""
    # SteamWebAPI endpoints
    GetPublishedFileDetails = "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"
    GetCollectionDetails = "https://api.steampowered.com/ISteamRemoteStorage/GetCollectionDetails/v1/"
    GetUGCFileDetails = "https://api.steampowered.com/ISteamRemoteStorage/GetUGCFileDetails/v1/"

    # Load SteamWebAPI Key
    with open("./SteamWebAPI.key", "r") as KeyFile:
        Key = KeyFile.read()
    LoadAttempts = 1000
    # Load Workshop Page Details
    for _ in trange(LoadAttempts, desc="Loading PublishedFileDetails"):
        try:
            GetPublishedFileDetailsData = {"key": Key, "itemcount": 1, "publishedfileids[0]": WorkshopID}
            GetPublishedFileDetailsRaw = requests.post(url=GetPublishedFileDetails, data=GetPublishedFileDetailsData)
            PublishedFileDetails = json.loads(GetPublishedFileDetailsRaw.text)["response"]["publishedfiledetails"][0]
        except json.JSONDecodeError:
            time.sleep(30)
            continue
        break
    if "result" in PublishedFileDetails:
        return
    CreatorAppID = str(PublishedFileDetails["creator_app_id"])
    ConsumerAppID = str(PublishedFileDetails["consumer_app_id"])

    # Load Collection Metadata
    if IsCollection:
        for _ in trange(LoadAttempts, desc="Loading CollectionDetails"):
            try:
                GetCollectionDetailsData = {"key": Key, "collectioncount": 1, "publishedfileids[0]": WorkshopID}
                GetCollectionDetailsRaw = requests.post(url=GetCollectionDetails, data=GetCollectionDetailsData)
                CollectionDetails = json.loads(GetCollectionDetailsRaw.text)["response"]["collectiondetails"][0]
            except json.JSONDecodeError:
                time.sleep(30)
                continue
            break

    # Get additional UGC metadata for the file
    if "file_url" in PublishedFileDetails and PublishedFileDetails["file_url"] != "":
        for _ in trange(LoadAttempts, desc="Loading PublishedFileDetailsFile"):
            try:
                GetUGCFileDetailsParametersFile = "?key=" + Key + "&ugcid=" + PublishedFileDetails["hcontent_file"] + "&appid=" + CreatorAppID
                GetUGCFileDetailsRawFile = requests.get(url=GetUGCFileDetails + GetUGCFileDetailsParametersFile)
            except json.JSONDecodeError:
                time.sleep(30)
                continue
            break
        if "data" in json.loads(GetUGCFileDetailsRawFile.text):
            UGCFileDetailsFile = (json.loads(GetUGCFileDetailsRawFile.text))["data"]
        else:
            for _ in trange(LoadAttempts, desc="Loading PublishedFileDetailsFile from Fallback ID"):
                try:
                    GetUGCFileDetailsParametersFile = "?key=" + Key + "&ugcid=" + PublishedFileDetails["hcontent_file"] + "&appid=" + ConsumerAppID
                    GetUGCFileDetailsRawFile = requests.get(url=GetUGCFileDetails + GetUGCFileDetailsParametersFile)
                    UGCFileDetailsFile = (json.loads(GetUGCFileDetailsRawFile.text))["data"]
                except json.JSONDecodeError:
                    time.sleep(30)
                    continue
                break

    # Get additional UGC metadata for the preview
    if "preview_url" in PublishedFileDetails and PublishedFileDetails["preview_url"] != "":
        for _ in trange(LoadAttempts, desc="Loading PublishedFileDetailsPreview"):
            try:
                GetUGCFileDetailsParametersPreview = "?key=" + Key + "&ugcid=" + PublishedFileDetails["hcontent_preview"] + "&appid=" + CreatorAppID
                GetUGCFileDetailsRawPreview = requests.get(url=GetUGCFileDetails + GetUGCFileDetailsParametersPreview)
                if "data" in json.loads(GetUGCFileDetailsRawPreview.text):
                    UGCFileDetailsPreview = (json.loads(GetUGCFileDetailsRawPreview.text))["data"]
            except json.JSONDecodeError:
                time.sleep(30)
                continue
            break
        else:
            for _ in trange(LoadAttempts, desc="Loading PublishedFileDetailsPreview from Fallback ID"):
                try:
                    GetUGCFileDetailsParametersPreview = "?key=" + Key + "&ugcid=" + PublishedFileDetails["hcontent_preview"] + "&appid=" + ConsumerAppID
                    GetUGCFileDetailsRawPreview = requests.get(url=GetUGCFileDetails + GetUGCFileDetailsParametersPreview)
                    if "data" in json.loads(GetUGCFileDetailsRawPreview.text):
                        UGCFileDetailsPreview = (json.loads(GetUGCFileDetailsRawPreview.text))["data"]
                except json.JSONDecodeError:
                    time.sleep(30)
                    continue
                break

    # Get Variables for Output
    SteamID64 = PublishedFileDetails["creator"]
    DateCreated = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc) + datetime.timedelta(seconds=PublishedFileDetails["time_created"])
    DateCreatedISO8601 = DateCreated.strftime("%Y-%m-%dT%H-%M-%S")
    WorkshopTitle = PublishedFileDetails["title"]

    # File Directory Variables
    if "file_url" in PublishedFileDetails and PublishedFileDetails["file_url"] != "":
        FileName = UGCFileDetailsFile["filename"]
        FileDirectories = FileName.split("/")
        FileName = FileDirectories[-1]
        # Remove the actual FileName, leaving only the directories.
        FileDirectories.pop(-1)

    # Preview Directory Variables
    if "preview_url" in PublishedFileDetails and PublishedFileDetails["preview_url"] != "":
        PreviewName = UGCFileDetailsPreview["filename"]
        PreviewDirectories = PreviewName.split("/")
        PreviewName = PreviewDirectories[-1]
        # Remove the actual PreviewName, leaving only the directories.
        PreviewDirectories.pop(-1)

    # Output Directory Creation
    OutputDirectory = "./Workshop-Downloads/" + str(SteamID64) + "/" + ConsumerAppID + "/" + DateCreatedISO8601 + " - " + WorkshopTitle + "/"
    if "file_url" in PublishedFileDetails and PublishedFileDetails["file_url"] != "":
        FileOutputDirectory = OutputDirectory
        for FileDirectory in FileDirectories:
            FileOutputDirectory += FileDirectory + "/"
    if "preview_url" in PublishedFileDetails and PublishedFileDetails["preview_url"] != "":
        PreviewOutputDirectory = OutputDirectory
        for PreviewDirectory in PreviewDirectories:
            PreviewOutputDirectory += PreviewDirectory + "/"
    os.makedirs(sanitize_filepath(OutputDirectory), exist_ok=True)
    if "file_url" in PublishedFileDetails and PublishedFileDetails["file_url"] != "":
        os.makedirs(sanitize_filepath(FileOutputDirectory), exist_ok=True)
    if "preview_url" in PublishedFileDetails and PublishedFileDetails["preview_url"] != "":
        os.makedirs(sanitize_filepath(PreviewOutputDirectory), exist_ok=True)

    # Download UGC Files
    if "file_url" in PublishedFileDetails and PublishedFileDetails["file_url"] != "":
        LocalFileLocation = sanitize_filepath(FileOutputDirectory + FileName)
        with requests.get(UGCFileDetailsFile["url"]) as RawFileContent, open(LocalFileLocation, "wb") as LocalFile, open(sanitize_filepath(LocalFileLocation + ".headers.json"), "w") as FileContentHeadersOutput:
            LocalFile.write(RawFileContent.content)
            json.dump(dict(RawFileContent.headers), FileContentHeadersOutput, sort_keys=True, indent=4)

    if "preview_url" in PublishedFileDetails and PublishedFileDetails["preview_url"] != "":
        LocalPreviewLocation = sanitize_filepath(PreviewOutputDirectory + PreviewName)
        with requests.get(UGCFileDetailsPreview["url"]) as RawPreviewContent, open(LocalPreviewLocation, "wb") as LocalPreview, open(sanitize_filepath(LocalPreviewLocation + ".headers.json"), "w") as PreviewContentHeadersOutput:
            LocalPreview.write(RawPreviewContent.content)
            json.dump(dict(RawPreviewContent.headers), PreviewContentHeadersOutput, sort_keys=True, indent=4)

    # Save JSON Responses
    PublishedFileDetailsOutput = open(sanitize_filepath(OutputDirectory + "/PublishedFileDetails.json"), "w")
    json.dump(PublishedFileDetails, PublishedFileDetailsOutput, sort_keys=True, indent=4)
    if "file_url" in PublishedFileDetails and PublishedFileDetails["file_url"] != "":
        UGCFileDetailsOutputFile = open(sanitize_filepath(OutputDirectory + "/UGCFileDetails.file.json"), "w")
        json.dump(UGCFileDetailsFile, UGCFileDetailsOutputFile, sort_keys=True, indent=4)
    if "preview_url" in PublishedFileDetails and PublishedFileDetails["preview_url"] != "":
        UGCFileDetailsOutputPreview = open(sanitize_filepath(OutputDirectory + "/UGCFileDetails.preview.json"), "w")
        json.dump(UGCFileDetailsPreview, UGCFileDetailsOutputPreview, sort_keys=True, indent=4)
    if IsCollection:
        CollectionDetailsOutput = open(sanitize_filepath(OutputDirectory + "/CollectionDetails.json"), "w")
        json.dump(CollectionDetails, CollectionDetailsOutput, sort_keys=True, indent=4)


if __name__ == "__main__":
    download(sys.argv[1])
