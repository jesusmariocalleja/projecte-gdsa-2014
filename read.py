# -*- coding: utf-8 -*-

import sys
import csv
import glob

# This lines increases the csv's line max size
csv.field_size_limit(sys.maxsize)


def readImagesFileNames(_path):
    imagesList = []
    imgL = glob.glob(_path)
    for item in imgL:
        item = item.split('/')
        item = item[1].split('.')
        item = item[0]
        imagesList.append(item)
    return imagesList


def writeTags(_iFileName, _oFileName):
    oFile = open(_oFileName, 'wb')
    wr = csv.writer(oFile)
    with open(_iFileName) as f:
        reader = csv.reader(f)
        for row in reader:
            image_id = str(row).strip('[ \' ]').split(r' ')
            image_id = image_id[0]
            for image in evalImages:
                if image == image_id:
                    wr.writerow(row)
                    break


def writeGroundTruth(_iFileName, _oFileName):
    oFile = open(_oFileName, 'wb')
    wr = csv.writer(oFile)
    with open(_iFileName, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            image_id = str(row).strip('[ \' ]').split(r' ')
            image_id = image_id[0]
            for image in evalImages:
                if image == image_id:
                    wr.writerow(row)
                    break


######################
#### MAIN PROGRAM ####
######################

#FILES VARS
images_path = "images/*"
main_id_tag_filename = "id_tag/document_id_tag.csv"
eval_id_tag_filename = "id_tag/evaluable_document_id_tag.csv"
main_groundtruth_filename = "groundtruth/groundtruth.csv"
eval_groundtruth_filename = "groundtruth/evaluable_groundtruth.csv"

print("Reading image names...")
evalImages = readImagesFileNames(images_path)

print("Writing image-tags file...")
writeTags(main_id_tag_filename, eval_id_tag_filename)

print("Writing groundtruth file...")
writeGroundTruth(main_groundtruth_filename, eval_groundtruth_filename)
