import json
import requests
import WorkshopDL
import sys
import time


def search(QueryType,ConsumerAppID,RequiredFlags,FileType,RequiredTags=""):
    """Searches the Steam Workshop"""
    # SteamWebAPI endpoint
    QueryFiles = "https://api.steampowered.com/IPublishedFileService/QueryFiles/v1/"

    # Timeout Variable
    LoadAttempts = 1000

    # Load SteamWebAPI Key
    with open("./SteamWebAPI.key", "r") as KeyFile:
        Key = KeyFile.read()
    QueryResults = []
    # Load Workshop Page Details
    for _ in range(LoadAttempts):
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
            time.sleep(3600)
            continue
        break
    QueryResults.append(QueryResult)
    Cursor = QueryResult["next_cursor"]
    TotalItems = QueryResult["total"]
    for unused in range(TotalItems):
        for _ in range(LoadAttempts):
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
                time.sleep(3600)
                continue
            break
        if QueryResult["total"] == 0:
            break
        Cursor = QueryResult["next_cursor"]
        QueryResults.append(QueryResult)
    print(json.dumps(QueryResults, sort_keys=True, indent=4))


if __name__ == "__main__":
    search(1, 213630, "", 0)
