# Spence! 2022
# commonspence.com

import json
import numpy
import os
import pandas
import random
import re
import requests
import time

from bs4 import BeautifulSoup
from pandasgui import show
from pprint import pprint
from urllib.parse import urlparse

################################################
################################################
# Report on locally stored Cities:Skylines assets
################################################
################################################

################################################
# change these properties locally with your own paths/collection info
################################################
# the path to the local C:S assets directory 
localDataFolder = "C:\\Users\\Spence\\AppData\\Local\\Colossal Order\\Cities_Skylines\\Addons\\Assets\\"
# info about collections we want to report on - steam workshop ID, readable name for the datatable, the local asset path on disk
collectionInfos = [
    {"id":"1127486361", "name":"shared buildings", "localPath":localDataFolder + "shared\\bldg"},
    {"id":"1127478101", "name":"shared props", "localPath":localDataFolder + "shared\\prop"},
    {"id":"1127479099", "name":"shared decals", "localPath":localDataFolder + "shared\\decal"},
    {"id":"1414918409", "name":"shared networks", "localPath":localDataFolder + "shared\\net"}
    ]

# how long to (randomly) wait in between each request, when there are multiple collections
sleepTime = (1.5, 3.0)



################################################
# evaluate a workshop collection item (a single item entry within the workshop page)
################################################
def evaluate_collection_item(localAssets, item, collectionID, collectionName):
    # extract the item ID from the query component of the item's URL
    wsURL = item.find(class_='workshopItem').a.get('href')
    u = urlparse(wsURL)
    itemID = idPattern.findall(u.query)[0]

    # get the collectionItemDetails element and extract associated properties
    wsDetails = item.find(class_='collectionItemDetails')
    itemTitle = wsDetails.find(class_='workshopItemTitle').get_text()
    author  = wsDetails.find(class_='workshopItemAuthor').get_text()
    itemAuthor = authorPattern.findall(author)[0]   # extract the author from the formatted string

    # evaluate whether there's a corresponding dir for this item somewhere within the localAssets dir
    if itemID in localAssets:
        itemExistsLocally = True;
    else:
        itemExistsLocally = False;


    # format current item properties as dict
    thisItem = {
                'collectionID':collectionID, 
                'collectionName':collectionName, 
                'itemTitle':itemTitle, 
                'itemAuthor':itemAuthor, 
                'itemID':itemID, 
                'itemExistsLocally':itemExistsLocally
                }

    return thisItem;

################################################
# get a workshop collection page and evaluate it
################################################
def evaluate_collection(collection):
    # the current id, local dir path
    id = collection["id"]
    localPath = collection["localPath"]

    # request and download the page data for this collection
    url = ('https://steamcommunity.com/sharedfiles/filedetails/?id=' + id)
    print("Getting page " + url) 
    pageDownload = requests.get(url)
    print("Got status code " + str(pageDownload.status_code))

    # parse the downloaded page data as HTML
    page = BeautifulSoup(pageDownload.content, 'html.parser')

    # get every collectionItem element
    items = page.find_all(class_='collectionItem')

    # walk the local dir path to gather directory names (local assets)
    localAssets = list()
    print("checking local asset dirs in " + localPath)
    for root, dirs, files in os.walk(localPath, topdown=False):
        for pathname in dirs:
            localAssets.append(pathname)
            print("adding local asset dir " + pathname)

    # create an empty pandas dataframe to contain each item associated with this collection
    collectionItemsDataframe = pandas.DataFrame(data=None, index=None, columns = ['collectionID', 'collectionName','itemID','itemTitle','itemAuthor','itemExistsLocally'])

    # evaluate each collectionItem and append results to the wider collectionItemsDataframe
    for item in items:
        thisItemData = evaluate_collection_item(localAssets, item, id, collection["name"])
        thisItemDataframe = pandas.DataFrame(thisItemData,index=[0])

        collectionItemsDataframe = collectionItemsDataframe.append(thisItemDataframe, ignore_index=True)

        pprint(thisItemData)

    return collectionItemsDataframe



################################################
# request each collection page, evaluate them, and generate/display the combined report
################################################
# precompile the regex search patterns
idPattern = re.compile(r'\d+') # extract digits
authorPattern = re.compile(r'(?:Created by[\t]+)(.+)(?:\n*)') # extract the author name 

# create an empty dataframe to contain the report contents
reportDataframe = pandas.DataFrame(data=None, index=None, columns = ['itemID','itemTitle','itemAuthor','itemExistsLocally'])


for info in collectionInfos:
        time.sleep(random.uniform(sleepTime[0], sleepTime[1]))
        collectionDataframe = evaluate_collection(info)
        reportDataframe = reportDataframe.append(collectionDataframe, ignore_index=True)

# use pandasgui to display the combined reportDataframe
show(reportDataframe)
