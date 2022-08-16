import json
import sys
import datetime
import requests
import os

#SteamWebAPI endpoints
GetPublishedFileDetails = "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"
GetCollectionDetails = "https://api.steampowered.com/ISteamRemoteStorage/GetCollectionDetails/v1/"
GetUGCFileDetails = "https://api.steampowered.com/ISteamRemoteStorage/GetUGCFileDetails/v1/"

#Load SteamWebAPI Key
KeyFile = open("./SteamWebAPI.key", "r")
Key = KeyFile.read()
KeyFile.close()

#Load Workshop Page Details
WorkshopID = str(sys.argv[1])
GetPublishedFileDetailsData = {"key":Key,"itemcount":1,"publishedfileids[0]":WorkshopID}
GetPublishedFileDetailsRaw = requests.post(url = GetPublishedFileDetails, data = GetPublishedFileDetailsData)
PublishedFileDetails = json.loads(GetPublishedFileDetailsRaw.text)["response"]["publishedfiledetails"][0]

print(json.dumps(PublishedFileDetails, sort_keys=True, indent=4))

#Get additional UGC metadata for the file
CreatorAppID = str(PublishedFileDetails["creator_app_id"])
GetUGCFileDetailsParametersFile = "?key=" + Key + "&ugcid=" + PublishedFileDetails["hcontent_file"] + "&appid=" + CreatorAppID
GetUGCFileDetailsRawFile = requests.get(url = GetUGCFileDetails + GetUGCFileDetailsParametersFile)
UGCFileDetailsFile = (json.loads(GetUGCFileDetailsRawFile.text)["data"])

print(json.dumps(UGCFileDetailsFile, sort_keys=True, indent=4))


#Get additional UGC metadata for the preview
GetUGCFileDetailsParametersPreview = "?key=" + Key + "&ugcid=" + PublishedFileDetails["hcontent_preview"] + "&appid=" + CreatorAppID
GetUGCFileDetailsRawPreview = requests.get(url = GetUGCFileDetails + GetUGCFileDetailsParametersPreview)
UGCFileDetailsPreview = (json.loads(GetUGCFileDetailsRawPreview.text)["data"])

print(json.dumps(UGCFileDetailsPreview, sort_keys=True, indent=4))


#Get Variables for Output
ConsumerAppID = str(PublishedFileDetails["consumer_app_id"])
SteamID64 = PublishedFileDetails["creator"]
DateCreated = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc) + datetime.timedelta(seconds=PublishedFileDetails["time_created"])
DateCreatedISO8601 = DateCreated.strftime("%Y-%m-%dT%H-%M-%S")
WorkshopTitle = PublishedFileDetails["title"]

#File Directory Variables
FileName = UGCFileDetailsFile["filename"]
FileDirectories = FileName.split("/")
FileName = FileDirectories[-1]
#Remove the actual FileName, leaving only the directories.
FileDirectories.pop(-1)

#Preview Directory Variables
PreviewName = UGCFileDetailsPreview["filename"]
PreviewDirectories = PreviewName.split("/")
PreviewName = PreviewDirectories[-1]
#Remove the actual PreviewName, leaving only the directories.
PreviewDirectories.pop(-1)

#Output Directory Creation
OutputDirectory = "./Workshop-Downloads/" + str(SteamID64) + "/" + ConsumerAppID + "/" + DateCreatedISO8601 + " - " + WorkshopTitle + "/"
FileOutputDirectory = OutputDirectory
for FileDirectory in FileDirectories:
    FileOutputDirectory += FileDirectory + "/"
PreviewOutputDirectory = OutputDirectory
for PreviewDirectory in PreviewDirectories:
    PreviewOutputDirectory += PreviewDirectory + "/"
os.makedirs(OutputDirectory, exist_ok = True)
os.makedirs(FileOutputDirectory, exist_ok = True)
os.makedirs(PreviewOutputDirectory, exist_ok = True)

#Download UGC Files
os.system("wget -O \"" + FileOutputDirectory + FileName + "\" " + UGCFileDetailsFile["url"])
os.system("wget -O \"" + PreviewOutputDirectory + PreviewName + "\" " + UGCFileDetailsPreview["url"])

#Save JSON Responses
PublishedFileDetailsOutput = open(OutputDirectory + "/PublishedFileDetails.json", "w")
json.dump(PublishedFileDetails, PublishedFileDetailsOutput, sort_keys=True, indent=4)
UGCFileDetailsOutputFile = open(OutputDirectory + "/UGCFileDetails.file.json", "w")
json.dump(UGCFileDetailsFile, UGCFileDetailsOutputFile, sort_keys=True, indent=4)
UGCFileDetailsOutputPreview = open(OutputDirectory + "/UGCFileDetails.preview.json", "w")
json.dump(UGCFileDetailsPreview, UGCFileDetailsOutputPreview, sort_keys=True, indent=4)