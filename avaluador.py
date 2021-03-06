# -*- coding: utf-8 -*-

import csv
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
#import pickle


class event(object):
    id = ""
    name = ""
    precision = 0.0
    recall = 0.0
    f1Score = 0.0
    predictedPositives = 0
    realPositives = 0
    matched = 0

    def __init__(self, id, name):
        self.id = id
        self.name = name


class image(object):
    document_id = ""
    event_type = ""

    def __init__(self, document_id, event_type):
        self.document_id = document_id
        self.event_type = event_type


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
            itemList.append(image(splitted[0], splitted[1]))
    return itemList


def countTrueImagesByEvent(_imgList, _event):
    cont = 0
    for image in _imgList:
        if image.event_type == _event:
            cont += 1
    return cont


def evaluate(_rList, _vList, _k):
    vListLength = len(_vList)
    if (_k == "all" or _k > vListLength):
        _k = vListLength

    averagePrecision = 0.0
    averageRecall = 0.0
    averageF1Score = 0.0
    eventsCount = len(eventsList)

    for event in eventsList:
        print("Calculating for event '" + event.name + "'")
        predictedPositives = countTrueImagesByEvent(_vList, event.name)
        realPositives = countTrueImagesByEvent(_rList, event.name)
        cont = 0
        matched = 0

        for vImage in _vList:
            if cont >= _k:
                break
            cont += 1
            if vImage.event_type == event.name:
                for rImage in _rList:
                    if rImage.document_id == vImage.document_id:
                        if rImage.event_type == vImage.event_type:
                            matched += 1
                        break

        event.predictedPositives = predictedPositives
        event.realPositives = realPositives
        event.matched = matched

        #Precision
        if predictedPositives == 0:
            event.precission = 0
        else:
            event.precision = ((float(matched) / float(predictedPositives)))
        averagePrecision += event.precision

        #Recall
        if realPositives == 0:
            event.recall = 0
        else:
            event.recall = ((float(matched) / float(realPositives)))
        averageRecall += event.recall

        #F1 Score
        if (event.precision + event.recall) == 0:
            event.f1Score = 0
        else:
            event.f1Score = ((2.0 * ((event.precision * event.recall) / (event.precision + event.recall))))
        averageF1Score += event.f1Score

        # print("Predicted Positives: " + str(predictedPositives))
        # print("Real Positives: " + str(realPositives))
        # print("Matched: " + str(matched))

    averagePrecision /= eventsCount
    averageRecall /= eventsCount
    averageF1Score /= eventsCount

    return [averagePrecision, averageRecall, averageF1Score]


def calcAccuracy(_rList, _vList, _k):
    hits = 0
    cont = 0

    if _k == "all":
        _k = len(_vList)

    for vImage in _vList:
        if cont >= _k:
            break
        cont += 1
        for rImage in _rList:
            if rImage.document_id == vImage.document_id:
                if rImage.event_type == vImage.event_type:
                    hits += 1
                break

    return float(hits) / float(len(_vList))


def calcMistakesAndMatches(_rList, _vList, _k):
    mistakes = 0
    matches = 0
    cont = 0

    if _k == "all":
        _k = len(_vList)

    for vImage in _vList:
        if cont >= _k:
            break
        cont += 1
        for rImage in _rList:
            if rImage.document_id == vImage.document_id:
                if rImage.event_type != vImage.event_type:
                    mistakes += 1
                else:
                    matches += 1
                break
    return [mistakes, matches]


def writeResults(_fileName):
    oFile = open(_fileName, 'wb')
    wr = csv.writer(oFile)

    wr.writerow(["Precission: " + ("%.4f" % results[0])])
    wr.writerow(["Recall: " + ("%.4f" % results[1])])
    wr.writerow(["F1 Score: " + ("%.4f" % results[2])])
    wr.writerow(["Accuracy: " + ("%.4f" % results[3])])
    wr.writerow(["Mistakes: " + (str(results[4]))])
    wr.writerow(["Matches: " + (str(results[5]))])

    for event in eventsList:
        wr.writerow([
            str(event.id)
            + "  " + event.name
            + "  " + ("%.4f" % event.precision)
            + "  " + ("%.4f" % event.recall)
            + "  " + ("%.4f" % event.f1Score)
        ])


def printResults():
    print("GLOBAL RESULTS")
    print("Precission: " + ("%.4f" % results[0]))
    print("Recall: " + ("%.4f" % results[1]))
    print("F1 Score: " + ("%.4f" % results[2]))
    print("Accuracy: " + ("%.4f" % results[3]))
    print("Mistakes: " + (str(results[4])))
    print("Matches: " + (str(results[5])))

    print("\n")
    print("RESULTS FOR EACH EVENT")
    print("EVENT ID     " 
        + "EVENT NAME        "
        + "PRECISION         "
        + "RECALL            "
        + "F1 SCORE          "
        + "PRED. POS.        "
        + "REAL POS.         "
        + "MATCHED           "
        + "MISTAKES")

    for event in eventsList:
        nameRestChars = 18 - len(event.name)
        realPosRestChars = 18 - len(str(event.predictedPositives))
        matchedRestChars = 18 - len(str(event.realPositives))
        mistakesRestChars = 18 - len(str(event.matched))
        nameSpace = ""
        realPosSpace = ""
        matchedSpace = ""
        mistakesSpace = ""
        for i in range(0, nameRestChars):
            nameSpace += " "
        for i in range(0, realPosRestChars):
            realPosSpace += " "
        for i in range(0, matchedRestChars):
            matchedSpace += " "
        for i in range(0, mistakesRestChars):
            mistakesSpace += " "
        print(str(event.id)
            + "            " + event.name
            + nameSpace + ("%.4f" % event.precision)
            + "            " + ("%.4f" % event.recall)
            + "            " + ("%.4f" % event.f1Score)
            + "            " + (str(event.predictedPositives))
            + realPosSpace + (str(event.realPositives))
            + matchedSpace + (str(event.matched))
            + mistakesSpace + (str(event.predictedPositives - event.matched))
        )


def printGraphs():
    y_pos = np.arange(len(eventsNames))
    precision = []
    recall = []
    mistakes = []
    for event in eventsList:
        precision.append(event.precision)
        recall.append(event.recall)
        mistakes.append(event.predictedPositives - event.matched)
    
    #Precision
    plt.barh(y_pos, precision, align='center', color="#1abc9c")
    plt.yticks(y_pos, eventsNames)
    plt.xlabel('Precision')
    plt.title('Precision for each class')
    plt.show()

    #Recall
    plt.barh(y_pos, recall, align='center', color="#9b59b6")
    plt.yticks(y_pos, eventsNames)
    plt.xlabel('Recall')
    plt.title('Recall for each class')
    plt.show()

    #Mistakes
    plt.barh(y_pos, mistakes, align='center', color="#e74c3c")
    plt.yticks(y_pos, eventsNames)
    plt.xlabel('Mistakes')
    plt.title('Mistakes for each class')
    plt.show()





######################
#### MAIN PROGRAM ####
######################

# FILES VARS
referenceFileName = "groundtruth/groundtruth_1.csv"  # "groundtruth/evaluable_groundtruth.csv" # Arxiu de la solució per comparar els resultats.
evaluableFileName = "classified.txt"  # Arxiu a evaluar.
resultsFileName = "results.txt"  # Arxiu on escriurem els resultats.

# Setting the K value
k = "all"  # Set k to "all" if we want to analyse all the values

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
print("Initializing the events")
eventsList = initEvents(eventsNames)

#Load the reference and evaluable list
print("Reading the reference 'image - event' table from the file '" + referenceFileName + "'")
referenceList = getData(referenceFileName)

print("Reading the evaluable 'image - event' table from the file '" + evaluableFileName + "'")
evaluableList = getData(evaluableFileName)

print("\n")
print("Starting to calculate...")
results = evaluate(referenceList, evaluableList, k)
results.append(calcAccuracy(referenceList, evaluableList, k))
mistakes_matches = calcMistakesAndMatches(referenceList, evaluableList, k)
mistakes = mistakes_matches[0]
matches = mistakes_matches[1]
results.append(mistakes)
results.append(matches)

print("\n")
print("Writing the obtained results in the file '" + resultsFileName + "'")
writeResults(resultsFileName)

print("\n")
printResults()
print("\n")

print("Printing graphs...")
print("\n")
printGraphs()
print("\n")
