import json
import requests
import urllib.parse
import time
from tqdm.auto import trange
import WorkshopDL


def search(QueryType,ConsumerAppID,RequiredFlags,RequiredTags=""):
    """Searches the Steam Workshop"""
    # SteamWebAPI endpoint
    QueryFiles = "https://api.steampowered.com/IPublishedFileService/QueryFiles/v1/"

    # Timeout Variable
    LoadAttempts = 1000

    # Load SteamWebAPI Key
    with open("./SteamWebAPI.key", "r") as KeyFile:
        Key = KeyFile.read()
    QueryResults = []
    FullResults = {}
    FileTypeCount = 20
    FileTypes = ["k_PFI_MatchingFileType_Items", "k_PFI_MatchingFileType_Collections", "k_PFI_MatchingFileType_Art", "k_PFI_MatchingFileType_Videos", "k_PFI_MatchingFileType_Screenshots", "k_PFI_MatchingFileType_CollectionEligible", "k_PFI_MatchingFileType_Games", "k_PFI_MatchingFileType_Software", "k_PFI_MatchingFileType_Concepts", "k_PFI_MatchingFileType_GreenlightItems", "k_PFI_MatchingFileType_AllGuides", "k_PFI_MatchingFileType_WebGuides", "k_PFI_MatchingFileType_IntegratedGuides", "k_PFI_MatchingFileType_UsableInGame", "k_PFI_MatchingFileType_Merch", "k_PFI_MatchingFileType_ControllerBindings", "k_PFI_MatchingFileType_SteamworksAccessInvites", "k_PFI_MatchingFileType_Items_Mtx", "k_PFI_MatchingFileType_Items_ReadyToUse", "k_PFI_MatchingFileType_WorkshopShowcase", "k_PFI_MatchingFileType_GameManagedItems"]
    # Load Workshop Page Details
    for FileType in trange(FileTypeCount, desc="Checking All FileTypes"):
        for _ in trange(LoadAttempts, desc="Loading First Result"):
            try:
                QueryFilesDict = {
                    "query_type": int(QueryType),
                    "cursor": "*",
                    "appid": ConsumerAppID,
                    "requiredtags": RequiredTags,
                    "required_flags": RequiredFlags,
                    "filetype": int(FileType),
                    "return_vote_data": True,
                    "return_tags": True,
                    "return_kv_tags": True,
                    "return_previews": True,
                    "return_children": True,
                    "return_short_description": True,
                    "return_for_sale_data": True,
                    "return_metadata": True
                }
                QueryFilesParameters = "?key=" + Key + "&input_json=" + json.dumps(QueryFilesDict)
                QueryFilesRaw = requests.get(url=QueryFiles + QueryFilesParameters)
                QueryResult = json.loads(QueryFilesRaw.text)["response"]
            except json.JSONDecodeError:
                time.sleep(30)
                continue
            break
        if "publishedfiledetails" in QueryResult:
            WorkshopDL.download(QueryResult["publishedfiledetails"][0]["publishedfileid"])
        QueryResults.append(QueryResult)
        Cursor = QueryResult["next_cursor"]
        TotalItems = QueryResult["total"]
        for Item in trange(TotalItems, desc="Loading All " + FileTypes[FileType] + " Results"):
            for _ in trange(LoadAttempts, desc="Loading Result #" + str(Item)):
                try:
                    QueryFilesDict = {
                        "query_type": int(QueryType),
                        "cursor": Cursor,
                        "appid": ConsumerAppID,
                        "requiredtags": RequiredTags,
                        "required_flags": RequiredFlags,
                        "filetype": int(FileType),
                        "return_vote_data": True,
                        "return_tags": True,
                        "return_kv_tags": True,
                        "return_previews": True,
                        "return_children": True,
                        "return_short_description": True,
                        "return_for_sale_data": True,
                        "return_metadata": True
                    }
                    QueryFilesParameters = "?key=" + Key + "&input_json=" + json.dumps(QueryFilesDict)
                    QueryFilesRaw = requests.get(url=QueryFiles + QueryFilesParameters)
                    QueryResult = json.loads(QueryFilesRaw.text)["response"]
                except json.JSONDecodeError:
                    time.sleep(30)
                    continue
                break
            if QueryResult["total"] == 0:
                break
            if "publishedfiledetails" not in QueryResult:
                break
            Cursor = urllib.parse.quote(QueryResult["next_cursor"])
            WorkshopDL.download(QueryResult["publishedfiledetails"][0]["publishedfileid"])
            QueryResults.append(QueryResult)
        FullResults[FileTypes[FileType]] = QueryResults
        QueryResults = []
    with open("./" + str(ConsumerAppID) + ".search.json", "w") as JSONOutput:
        json.dump(FullResults, JSONOutput, sort_keys=True, indent=4)


if __name__ == "__main__":
    search(1, 213630, "")
