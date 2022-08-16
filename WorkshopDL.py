import json
import sys
import datetime
import requests
import os

def download(WorkshopID):
    #SteamWebAPI endpoints
    GetPublishedFileDetails = "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"
    GetCollectionDetails = "https://api.steampowered.com/ISteamRemoteStorage/GetCollectionDetails/v1/"
    GetUGCFileDetails = "https://api.steampowered.com/ISteamRemoteStorage/GetUGCFileDetails/v1/"

    #Load SteamWebAPI Key
    KeyFile = open("./SteamWebAPI.key", "r")
    Key = KeyFile.read()
    KeyFile.close()

    #Load Workshop Page Details
    GetPublishedFileDetailsData = {"key":Key,"itemcount":1,"publishedfileids[0]":WorkshopID}
    GetPublishedFileDetailsRaw = requests.post(url = GetPublishedFileDetails, data = GetPublishedFileDetailsData)
    PublishedFileDetails = json.loads(GetPublishedFileDetailsRaw.text)["response"]["publishedfiledetails"][0]
    CreatorAppID = str(PublishedFileDetails["creator_app_id"])
    ConsumerAppID = str(PublishedFileDetails["consumer_app_id"])

    print(json.dumps(PublishedFileDetails, sort_keys=True, indent=4))

    #Get additional UGC metadata for the file
    if "file_url" in PublishedFileDetails and PublishedFileDetails["file_url"] != "":
        GetUGCFileDetailsParametersFile = "?key=" + Key + "&ugcid=" + PublishedFileDetails["hcontent_file"] + "&appid=" + CreatorAppID
        GetUGCFileDetailsRawFile = requests.get(url = GetUGCFileDetails + GetUGCFileDetailsParametersFile)
        if "data" in json.loads(GetUGCFileDetailsRawFile.text):
            UGCFileDetailsFile = (json.loads(GetUGCFileDetailsRawFile.text))["data"]
        else:
            GetUGCFileDetailsParametersFile= "?key=" + Key + "&ugcid=" + PublishedFileDetails["hcontent_file"] + "&appid=" + ConsumerAppID
            GetUGCFileDetailsRawFile = requests.get(url = GetUGCFileDetails + GetUGCFileDetailsParametersFile)
            UGCFileDetailsFile = (json.loads(GetUGCFileDetailsRawFile.text))["data"]


    #Get additional UGC metadata for the preview
    if "preview_url" in PublishedFileDetails and PublishedFileDetails["preview_url"] != "":
        GetUGCFileDetailsParametersPreview = "?key=" + Key + "&ugcid=" + PublishedFileDetails["hcontent_preview"] + "&appid=" + CreatorAppID
        GetUGCFileDetailsRawPreview = requests.get(url = GetUGCFileDetails + GetUGCFileDetailsParametersPreview)
        if "data" in json.loads(GetUGCFileDetailsRawPreview.text):
            UGCFileDetailsPreview = (json.loads(GetUGCFileDetailsRawPreview.text))["data"]
        else:
            GetUGCFileDetailsParametersPreview = "?key=" + Key + "&ugcid=" + PublishedFileDetails["hcontent_preview"] + "&appid=" + ConsumerAppID
            GetUGCFileDetailsRawPreview = requests.get(url = GetUGCFileDetails + GetUGCFileDetailsParametersPreview)
            if "data" in json.loads(GetUGCFileDetailsRawPreview.text):
                UGCFileDetailsPreview = (json.loads(GetUGCFileDetailsRawPreview.text))["data"]


    #Get Variables for Output
    SteamID64 = PublishedFileDetails["creator"]
    DateCreated = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc) + datetime.timedelta(seconds=PublishedFileDetails["time_created"])
    DateCreatedISO8601 = DateCreated.strftime("%Y-%m-%dT%H-%M-%S")
    WorkshopTitle = PublishedFileDetails["title"]

    #File Directory Variables
    if "file_url" in PublishedFileDetails and PublishedFileDetails["file_url"] != "":
        FileName = UGCFileDetailsFile["filename"]
        FileDirectories = FileName.split("/")
        FileName = FileDirectories[-1]
        #Remove the actual FileName, leaving only the directories.
        FileDirectories.pop(-1)

    #Preview Directory Variables
    if "preview_url" in PublishedFileDetails and PublishedFileDetails["preview_url"] != "":
        PreviewName = UGCFileDetailsPreview["filename"]
        PreviewDirectories = PreviewName.split("/")
        PreviewName = PreviewDirectories[-1]
        #Remove the actual PreviewName, leaving only the directories.
        PreviewDirectories.pop(-1)

    #Output Directory Creation
    OutputDirectory = "./Workshop-Downloads/" + str(SteamID64) + "/" + ConsumerAppID + "/" + DateCreatedISO8601 + " - " + WorkshopTitle + "/"
    if "file_url" in PublishedFileDetails and PublishedFileDetails["file_url"] != "":
        FileOutputDirectory = OutputDirectory
        for FileDirectory in FileDirectories:
            FileOutputDirectory += FileDirectory + "/"
    if "preview_url" in PublishedFileDetails and PublishedFileDetails["preview_url"] != "":
        PreviewOutputDirectory = OutputDirectory
        for PreviewDirectory in PreviewDirectories:
            PreviewOutputDirectory += PreviewDirectory + "/"
    os.makedirs(OutputDirectory, exist_ok = True)
    if "file_url" in PublishedFileDetails and PublishedFileDetails["file_url"] != "":
        os.makedirs(FileOutputDirectory, exist_ok = True)
    if "preview_url" in PublishedFileDetails and PublishedFileDetails["preview_url"] != "":
        os.makedirs(PreviewOutputDirectory, exist_ok = True)

    #Download UGC Files
    if "file_url" in PublishedFileDetails and PublishedFileDetails["file_url"] != "":
        os.system("wget -O \"" + FileOutputDirectory + FileName + "\" " + UGCFileDetailsFile["url"])
    if "preview_url" in PublishedFileDetails and PublishedFileDetails["preview_url"] != "":
        os.system("wget -O \"" + PreviewOutputDirectory + PreviewName + "\" " + UGCFileDetailsPreview["url"])

    #Save JSON Responses
    PublishedFileDetailsOutput = open(OutputDirectory + "/PublishedFileDetails.json", "w")
    json.dump(PublishedFileDetails, PublishedFileDetailsOutput, sort_keys=True, indent=4)
    if "file_url" in PublishedFileDetails and PublishedFileDetails["file_url"] != "":
        UGCFileDetailsOutputFile = open(OutputDirectory + "/UGCFileDetails.file.json", "w")
        json.dump(UGCFileDetailsFile, UGCFileDetailsOutputFile, sort_keys=True, indent=4)
    if "preview_url" in PublishedFileDetails and PublishedFileDetails["preview_url"] != "":
        UGCFileDetailsOutputPreview = open(OutputDirectory + "/UGCFileDetails.preview.json", "w")
        json.dump(UGCFileDetailsPreview, UGCFileDetailsOutputPreview, sort_keys=True, indent=4)

if __name__ == '__main__':
    download(sys.argv[1])