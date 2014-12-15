# -*- coding: utf-8 -*-

import csv


class imageTags(object):
    document_id = ""
    tags_list = []

    def __init__(self, document_id, tags_list):
        self.document_id = document_id
        self.tags_list = tags_list


### XUS ###
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
        splitted = str(reader[0]).strip('[ \' ]').split(r'\t')
        itemList.append(imageTags(splitted[0], [splitted[1]]))

        # resta d'iteracions
        for row in reader:
            splitted = str(row).strip('[ \' ]').split(r'\t')
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
            tags += " " + tag
        wr.writerow([item.document_id+' '+tags])


### XUS ###
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
            splitted = str(row).strip('[ \' ]').split(r'\t')
            itemList.append(imageEvent(splitted[0], splitted[1]))
    del itemList[0]
    return itemList
##########


def createTF_IDF(_imageTagsList, _referenceList):
    for event in eventsList:
        tags = []
        for rImage in _referenceList:
            if rImage.event_type == event.name:
                for imageTags in _imageTagsList:
                    if imageTags.document_id == rImage.document_id:
                        for tag in imageTags.tags_list:
                            tags.append(tag)
                        break
        event.tags_list = tags


def writeTF_IDF():
    oFile = open("TFIDF.txt", 'wb')
    wr = csv.writer(oFile)
    for event in eventsList:
        tags = ""
        for tag in event.tags_list:
            tags += tag + ", "
        wr.writerow(["***" + event.name+"\n"+tags+"\n\n"])


######################
#### MAIN PROGRAM ####
######################

imageTagsList = getTags("sed2013_task2_dataset_train_tags.csv")

writeTags("id_tags.csv", imageTagsList)

### XUS ###
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


#Load the reference list
referenceList = getData("train.csv")
##########

createTF_IDF(imageTagsList, referenceList)
writeTF_IDF()
