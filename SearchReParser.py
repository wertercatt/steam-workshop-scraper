import json
import sys

import WorkshopDL


def reparse(filename):
    with open(filename) as jsonfile:
        SearchResults = json.load(jsonfile)
    for category in SearchResults:
        if SearchResults[category][0]["total"] != 0:
            for i in SearchResults[category]:
                if category == "k_PFI_MatchingFileType_Collections":
                    WorkshopDL.ExternalDetailsDownload(
                        i["publishedfiledetails"][0], IsCollection=True
                    )
                else:
                    WorkshopDL.ExternalDetailsDownload(i["publishedfiledetails"][0])


if __name__ == "__main__":
    reparse(sys.argv[1])
