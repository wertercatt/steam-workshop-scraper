#    Steam Workshop Item Downloader
#    Copyright (C) 2019  Blaze "wertercatt" Marshall
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
import json
import requests
import io
import os
from sys import argv
from datetime import datetime

key = 'A1A81C10144C6843539A230EDF00DCBC'
workshopID = argv[1]
tags = u''
endpoint = "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"
data = {'key':key,'itemcount':1,'publishedfileids[0]':workshopID}

r = requests.post(url = endpoint, data = data)
jsondata = r.json()

#Get the info we need from jsondata
#tagsDict = jsondata['response']['publishedfiledetails'][0]['tags']
for i in jsondata['response']['publishedfiledetails'][0]['tags']:
	tags = tags + u', ' + u",".join(i.values())
tags = tags[2:]
title = jsondata['response']['publishedfiledetails'][0]['title']
filename = jsondata['response']['publishedfiledetails'][0]['filename']
release = int(jsondata['response']['publishedfiledetails'][0]['time_created'])
update = int(jsondata['response']['publishedfiledetails'][0]['time_updated'])
SteamID64 = jsondata['response']['publishedfiledetails'][0]['creator']
description = jsondata['response']['publishedfiledetails'][0]['description']
gameID = jsondata['response']['publishedfiledetails'][0]['consumer_app_id']
file_url = jsondata['response']['publishedfiledetails'][0]['file_url']
preview_url = jsondata['response']['publishedfiledetails'][0]['preview_url']
authorrequest = requests.get(url = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/", params = {'key':key,'steamids':SteamID64})
authorjson = authorrequest.json()
author = authorjson['response']['players'][0]['personaname']
os.makedirs(str(gameID) + u'/' + str(workshopID) + u'/mymaps')
f = io.open(str(gameID) + u'/' + str(workshopID) + u'/' + str(filename) + '.txt', 'a', encoding='utf-8', newline='')
gamerequest = requests.get(url = "https://store.steampowered.com/api/appdetails", params = {'appids':gameID})
gamejson = gamerequest.json()
game = gamejson[str(gameID)]['data']['name']
#f.write(u'tags = ' + unicode(tags))
#f.write(u'title = ' + unicode(title))
#f.write(u'filename = ' + unicode(filename))
#f.write(u'release = ' + unicode(release))
#f.write(u'update = ' + unicode(update))
#f.write(u'SteamID64 = ' + unicode(SteamID64))
#f.write(u'description = ' + unicode(description))
#f.write(u'gameID = ' + unicode(gameID))

f.write(u'===========================================================================\n')
f.write(u'Tags\t\t\t\t\t: ' + unicode(tags) + u'\n')
f.write(u'===========================================================================\n')
f.write(u'Title\t\t\t\t\t: ' + unicode(title) + u'\n')
f.write(u'WorkshopID\t\t\t\t: ' + unicode(workshopID) + u'\n')
f.write(u'Filename\t\t\t\t: ' + unicode(filename) + u'\n')
f.write(u'Release date\t\t\t: ' + datetime.utcfromtimestamp(release).isoformat() + u'\n')
f.write(u'Update date\t\t\t\t: ' + datetime.utcfromtimestamp(update).isoformat() + u'\n')
f.write(u'Author\t\t\t\t\t: ' + unicode(author) + u'\n')
f.write(u'SteamID64\t\t\t\t: ' + unicode(SteamID64) + u'\n\n')
f.write(u'Description\t\t\t\t: ' + unicode(description) + u'\n\n')
f.write(u'===========================================================================\n* Play Information *\n')
f.write(u'Game\t\t\t\t\t: ' + unicode(game))

os.system(u'wget -O "' + str(gameID) + u'/' + str(workshopID) + u'/' + str(filename) + u'" "' + file_url + u'"')
os.system(u'wget -O "' + str(gameID) + u'/' + str(workshopID) + u'/' + str(filename) + u'_preview.png" "' + preview_url + u'"')