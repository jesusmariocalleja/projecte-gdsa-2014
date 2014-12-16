# -*- coding: utf-8 -*-

import sys
import csv


# This lines increases the csv's line max size
csv.field_size_limit(sys.maxsize)


class event(object):
    name = ""
    tags_list = []
    match_counter = 0

    def __init__(self, name, tags_list):
        self.name = name
        self.tags_list = tags_list


class image(object):
    document_id = ""
    tags_list = []
    event_type = ""

    def __init__(self, document_id, tags_list):
        self.document_id = document_id
        self.tags_list = tags_list


def getEventsTags(_fileName):
    with open(_fileName, 'rb') as f:
        eventsList = []
        reader = csv.reader(f)
        for row in reader:
            splitted = str(row).strip('[ \' ]').split(r'***')
            tagsList = splitted[1].split(r',')
            eventsList.append(event(splitted[0], tagsList))
    return eventsList


def getImages(_fileName):
    with open(_fileName, 'rb') as f:
        imagesList = []
        reader = csv.reader(f)
        for row in reader:
            splitted = str(row).strip('[ \' ]').split(r'***')
            tagsList = splitted[1].split(r',')
            imagesList.append(image(splitted[0], tagsList))
    return imagesList


def classify():
    cont = 1  # Aquestes variables (cont i length) són simplement pel text que es mostra a la consola.
    length = len(imagesList)

    oFile = open("classified.csv", 'wb')
    wr = csv.writer(oFile)

    wr.writerow(["document_id event_type"])  # Escribim la primera línia

    for image in imagesList:  # Per cada imatge
        print ("Classifying image " + image.document_id + " (" + str(cont) + " of " + str(length) + ")")
        for imageTag in image.tags_list:  # Agafem cadascún dels seus tags
            for event in eventsTagsList:
                match = 0
                for eventTag in event.tags_list:  # I el busquem a la llista de events-tags de l'event.
                    if eventTag == imageTag:  # Si troba el tag en aquell event, el comptador de l'event +1.
                        match += 1
                        break
                event.match_counter += match
        winner_counter = 0
        winner_event = ""
        for event in eventsTagsList:  # Aquí simplement mirem l'event amb el comptador més alt i li assignem a la imatge.
            if event.match_counter > winner_counter:
                winner_counter = event.match_counter
                winner_event = event.name
            event.match_counter = 0  # Un cop analitzat el comptador de l'event, el reiniciem per la següent imatge.
        if winner_counter == 0:  # Si una imatge no té cap event assignat, se li posa non_event.
            image.event_type = "non_event"
        else:
            image.event_type = winner_event

        wr.writerow([image.document_id + " " + image.event_type])
        cont += 1


######################
#### MAIN PROGRAM ####
######################

#FILES VARS
eventTagsFileName = "TF_IDF.csv"
evaluableImageTagsFileName = "id_tags.csv"


print("Getting events and related tags")
eventsTagsList = getEventsTags(eventTagsFileName)  # Llegim la llista on tenim tots els tags per cada event.

print("Getting images to classify")
imagesList = getImages(evaluableImageTagsFileName)  # Llegim la llista amb les imatges i els tags que ens passa el descriptor.

print("Starting to classify")
classify()

