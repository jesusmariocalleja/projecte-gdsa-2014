# -*- coding: utf-8 -*-

import sys
import csv

# Aquesta linea incrementa el tamany maxim de linea de csv
csv.field_size_limit(sys.maxsize)


class imageTags(object):
    document_id = ""
    tags_list = []

    def __init__(self, document_id, tags_list):
        self.document_id = document_id
        self.tags_list = tags_list


### FROM AVALUADOR ###
class event(object):
    id = ""
    name = ""
    tags_list = []

    def __init__(self, id, name):
        self.id = id
        self.name = name


class imageEvent(object):
    document_id = ""
    event_type = ""

    def __init__(self, document_id, event_type):
        self.document_id = document_id
        self.event_type = event_type
##########


def getTags(_fileName):
    with open(_fileName, 'rb') as f:
        itemList = []
        reader = list(csv.reader(f))
        i = 0

        # 1a iteració
        splitted = str(reader[0]).strip('[ \' ]').split(r'\t')  # \t for tabs
        itemList.append(imageTags(splitted[0], [splitted[1]]))

        # resta d'iteracions
        for row in reader:
            splitted = str(row).strip('[ \' ]').split(r'\t')  # \t for tabs
            if splitted[0] == itemList[i].document_id:
                itemList[i].tags_list.append(splitted[1])
            else:
                itemList.append(imageTags(splitted[0], [splitted[1]]))
                i += 1

    del itemList[0]  # esborrem la primera fila on trobem els títols
    return itemList


def writeTags(_fName, _data):
    oFile = open(_fName, 'wb')
    wr = csv.writer(oFile)
    for item in _data:
        tags = ""
        for tag in item.tags_list:
            tags += tag + ","
        wr.writerow([item.document_id + '***' + tags])


### FROM AVALUADOR ###
def initEvents(_events):
    eventsList = []
    i = 0
    for e in _events:
        eventsList.append(event(i, e))
        i += 1
    return eventsList


def getData(_fileName):
    with open(_fileName, 'rb') as f:
        itemList = []
        reader = csv.reader(f)
        for row in reader:
            splitted = str(row).strip('[ \' ]').split(r' ')  # \t for tabs
            itemList.append(imageEvent(splitted[0], splitted[1]))
    del itemList[0]
    return itemList
##########


def createTF_IDF(_imageTagsList, _referenceImageEventList):
    for event in eventsList:
        tags = []
        for rImage in _referenceImageEventList:
            if rImage.event_type == event.name:
                for imageTags in _imageTagsList:
                    if imageTags.document_id == rImage.document_id:
                        for tag in imageTags.tags_list:
                            tags.append(tag)
                        break
        event.tags_list = set(tags)  # Set elimina els duplicats en una llista


def writeTF_IDF():
    oFile = open("TF_IDF.csv", 'wb')
    wr = csv.writer(oFile)
    for event in eventsList:
        tags = ""
        for tag in event.tags_list:
            tags += tag + ","
        wr.writerow([event.name + "***" + tags])


######################
#### MAIN PROGRAM ####
######################

imageTagsList = getTags("document_id_tag_2.csv")

writeTags("id_tags.csv", imageTagsList)

### tipus d'events ###
eventsNames = [
    "concert",
    "conference",
    "exhibition",
    "fashion",
    "other",
    "protest",
    "sports",
    "theater_dance",
    "non_event"
]

#Init events
eventsList = initEvents(eventsNames)


#Carrega la llista de referencia
referenceImageTagsList = getTags("document_id_tag_1.csv")
referenceImageEventList = getData("train_1.csv")
###########


createTF_IDF(referenceImageTagsList, referenceImageEventList)
writeTF_IDF()
