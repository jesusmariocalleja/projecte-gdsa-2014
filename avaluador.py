# -*- coding: utf-8 -*-
import csv


class image(object):
    document_id = ""
    event_type = ""

    def __init__(self, document_id, event_type):
        self.document_id = document_id
        self.event_type = event_type


def getData(fileName):
    with open(fileName, 'rb') as f:
        itemList = []
        reader = csv.reader(f)
        for row in reader:
            splitted = str(row).strip('[ \' ]').split(r'\t')
            itemList.append(image(splitted[0], splitted[1]))
    del itemList[0]
    return itemList


def countImages(imagesList, event):
    cont = 0
    for image in imagesList:
        if image.event_type == event:
            cont += 1
    return cont


def writeData(fileName, data):
    oFile = open(fileName, 'wb')
    wr = csv.writer(oFile)
    for item in data:
        wr.writerow([item.document_id+' '+item.event_type])


######################
#### MAIN PROGRAM ####
######################

iFileName = "train.csv"

imagesList = getData(iFileName)

concert = countImages(imagesList, "concert")
conference = countImages(imagesList, "conference")
exhibition = countImages(imagesList, "exhibition")
fashion = countImages(imagesList, "fashion")
other = countImages(imagesList, "other")
protest = countImages(imagesList, "protest")
sports = countImages(imagesList, "sports")
theater_dance = countImages(imagesList, "theater_dance")
no_event = countImages(imagesList, "no_event")

print concert
print conference
print exhibition
print fashion
print other
print protest
print sports
print theater_dance
print no_event

#writeData("result.csv", imagesList)
