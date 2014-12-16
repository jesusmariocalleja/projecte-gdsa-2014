# -*- coding: utf-8 -*-

import csv


class event(object):
    id = ""
    name = ""
    precision = 0.0
    recall = 0.0
    f1Score = 0.0

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
    del itemList[0]
    return itemList


def countImages(_imgList, _event):
    cont = 0
    for image in _imgList:
        if image.event_type == _event:
            cont += 1
    return cont


def evaluate(_rList, _vList, _k):
    if _k == "all":
        _k = len(_vList)

    k_aux = 0
    averagePrecision = 0.0
    averageRecall = 0.0
    averageF1Score = 0.0
    eventCounter = 0

    for event in eventsList:

        print("Calculating for event '" + event.name + "'")
        M = countImages(_rList, event.name)  # Used to calculate Recall
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
        if _k > M:
            k_aux = M
        else:
            k_aux = _k
        event.precision = ((float(matched) / float(k_aux)))
        event.recall = ((float(matched) / float(M)))
        if (event.precision + event.recall) == 0:
            event.f1Score = 0
        else:
            event.f1Score = ((2.0 * ((event.precision * event.recall) / (event.precision + event.recall))))

        averagePrecision += event.precision
        averageRecall += event.recall
        averageF1Score += event.f1Score
        eventCounter += 1

    averagePrecision /= eventCounter
    averageRecall /= eventCounter
    averageF1Score /= eventCounter

    return [averagePrecision, averageRecall, averageF1Score]


def calcRelevantDocuments(_rList, _vList):
    cont = 1
    M = 0

    for vImage in _vList:
        for rImage in _rList:
            if rImage.document_id == vImage.document_id:
                if rImage.event_type == vImage.event_type:
                    M = cont
                break
        cont += 1

    return M


def evaluate2(_rList, _vList, _k):
    vListLength = len(_vList)
    if (_k == "all" or _k > vListLength):
        _k = vListLength

    cont = 0
    matched = 0

    for vImage in _vList:
        if cont >= _k:
                break
        cont += 1
        for rImage in _rList:
            if rImage.document_id == vImage.document_id:
                if rImage.event_type == vImage.event_type:
                    matched += 1
                break

    M = calcRelevantDocuments(_rList, _vList)

    precision = ((float(matched) / float(_k)))
    recall = ((float(matched) / float(M)))
    if (precision + recall) == 0:
        f1Score = 0.0
    else:
        f1Score = ((2.0 * ((precision * recall) / (precision + recall))))

    return [precision, recall, f1Score]


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


def writeResults(_fileName):
    oFile = open(_fileName, 'wb')
    wr = csv.writer(oFile)
    wr.writerow(["Precission: " + ("%.4f" % results[0])])
    wr.writerow(["Recall: " + ("%.4f" % results[1])])
    wr.writerow(["F1 Score: " + ("%.4f" % results[2])])
    wr.writerow(["Accuracy: " + ("%.4f" % results[3])])
    '''
    for event in eventsList:
        wr.writerow([
            str(event.id)
            + "  " + event.name
            + "  " + ("%.4f" % event.precision)
            + "  " + ("%.4f" % event.recall)
            + "  " + ("%.4f" % event.f1Score)
        ])
    '''


def printResults():
    print("GLOBAL RESULTS")
    print("Precission: " + ("%.4f" % results[0]))
    print("Recall: " + ("%.4f" % results[1]))
    print("F1 Score: " + ("%.4f" % results[2]))
    print("Accuracy: " + ("%.4f" % results[3]))

    '''
    print("\n")
    print("RESULTS FOR EACH EVENT")
    print("EVENT ID     EVENT NAME        PRECISSION        RECALL            F1 SCORE")
    for event in eventsList:
        nameRestChars = 18 - len(event.name)
        space = ""
        for i in range(0, nameRestChars):
            space += " "
        print(str(event.id)
            + "            " + event.name
            + space + ("%.4f" % event.precision)
            + "            " + ("%.4f" % event.recall)
            + "            " + ("%.4f" % event.f1Score)
        )
    '''


##########
## For Testing, this function returns if the image has the same event than the result image.
##########
def checkIfIsWellClassified(_rList, _vList, _k):
    result = False
    mistakes = 0
    oFile = open("same_result.txt", 'wb')
    wr = csv.writer(oFile)
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
                    result = True
                else:
                    result = False
                    mistakes += 1
                break
        wr.writerow([vImage.document_id+' '+str(result)])
    print("Número d'errades: " + str(mistakes))
##########


##########
## For Testing, this just writes the data we want to.
##########
def writeData(_fileName, _data):
    oFile = open(_fileName, 'wb')
    wr = csv.writer(oFile)
    for item in _data:
        # Here we write what we want
        eventName = item.event_type
        cont = 0
        #'''
        for event in eventsList:
            if event.name == eventName:
                cont = countImages(_data, eventName)
        #'''
        wr.writerow([item.document_id+' '+item.event_type+' '+str(cont)])
##########


######################
#### MAIN PROGRAM ####
######################

# FILES VARS
referenceFileName = "train_2.csv"  # Arxiu de la solució per comparar els resultats.
evaluableFileName = "classified.csv"  # Arxiu a evaluar.
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
#results = evaluate(referenceList, evaluableList, k)
results = evaluate2(referenceList, evaluableList, k)
results.append(calcAccuracy(referenceList, evaluableList, k))

print("\n")
print("Writing the obtained results in the file '" + resultsFileName + "'")
writeResults(resultsFileName)

print("\n")
printResults()
print("\n")


##########
## For Testing, this function returns if the image has the same event than the result image
##########
#checkIfIsWellClassified(referenceList, evaluableList, k)
##########
