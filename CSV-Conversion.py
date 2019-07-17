# shell commands with !
# ! pip install dicttoxml
import pandas as pd
import re
from dicttoxml import dicttoxml
import xml.etree.cElementTree as ET

# End imports
myFile = "data_in/BostonZipgradeCsv.csv"
data = pd.read_csv(myFile)
# data.head
# list(data) # show column names

str1 = "mystring"

# First...
# We generate the general structure of the XML fi
root = ET.Element("Manifest")
doc = ET.SubElement(root, "submission")
trainingprovider = ET.SubElement(doc,
                                 "trainingprovider",
                                 tpemail="testsetestsetstst@ruraltraining.org",
                                 tpid=str1,
                                 tpphone="6066776000")

trainingprovider.text = "res@ruraltraining.org"

structureClass = ET.SubElement(
    trainingprovider, "class",
    catalognum="AWR-144",
    classcity="Hoboken",
    classstate="NJ",
    classtype="I",
    classzipcode="07030",
    startdate="08102018",
    enddate="08102018",
    numstudent="40",
    trainingmethod="M",
    starttime="0900",
    endtime="1700",
    contacthours="8",
    preparerlastname="Melton",
    preparerfirstname="Jessica",
    batchpreparerphone="6066776000",
    batchprepareremail="res@ruraltraining.org")

ET.SubElement(
    structureClass,
    "instructorpoc",
    instlastname="Thomas",
    instfirstname="Laurie",
    instphone="6066776000",
    instemail="Laurie.Thomas@ruraltraining.org"
)

tagRegistration = ET.SubElement(structureClass, "registration")
tagEvaluations = ET.SubElement(structureClass, "evaluations")

# Make student records for registration section

# for each entry, run the following to sub in values
# and map data to an attribute
# https://cmdlinetips.com/2018/12/how-to-loop-through-pandas-rows-or-how-to-iterate-over-pandas-rows/

## TODO break this into a function
# loop through each
for index, row in data.iterrows():
    str_sid = str(row['StudentID'])
    ET.SubElement(tagRegistration, "student",
                  QuizCreated=str(row['QuizCreated']),
                  StudentID=str(row['StudentID']))
    # now make anonymized evalData
    evalDataItem = ET.SubElement(tagEvaluations, "evaldata")
    questionItem = ET.SubElement(evalDataItem, "question")

    # make a key/value pair for each item
    cols = list(row)
    # TODO break this into a function
    for field in cols:  ## cannot access the index
        fieldName = str(list(row)[index])
        fieldValue = str(row[fieldName])
        # fieldValueReplaced = str.replace('$', fieldValue)
        print(fieldName)
        if fieldName != fieldName:
            # questionItem.set(fieldName, fieldValue)
            print(fieldName, fieldValue)
    # Make student records for evaluation section
tree = ET.ElementTree(root)
tree.write("data_out/dataout.xml", encoding="utf-8", xml_declaration=True)
