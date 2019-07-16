# shell commands with !
# ! pip install dicttoxml
# https://towardsdatascience.com/the-easy-way-to-work-with-csv-json-and-xml-in-python-5056f9325ca9
import pandas as pd
from dicttoxml import dicttoxml

myFile = "data_in/BostonZipgradeCsv.csv"
data = pd.read_csv(myFile)
data.head
list(data)

# https://stackoverflow.com/questions/18574108/how-do-convert-a-pandas-dataframe-to-xml
# use ElementTree
# https://docs.python.org/2/library/xml.etree.elementtree.html
import xml.etree.cElementTree as ET

str1 = "mystring"

## First...
# We generate the general structure of the XML fi
root = ET.Element("Manifest")
doc = ET.SubElement(root, "submission")
trainingprovider = ET.SubElement(doc,
                                 "trainingprovider",
                                 tpemail="testsetestsetstst@ruraltraining.org",
                                 tpid=str1,
                                 tpphone="6066776000")

trainingprovider.text = "res@ruraltraining.org"

structureClass = ET.SubElement(trainingprovider, "class",
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

ET.SubElement(structureClass, "instructorpoc",
              instlastname="Thomas",
              instfirstname="Laurie",
              instphone="6066776000",
              instemail="Laurie.Thomas@ruraltraining.org"
              )

tagRegistration = ET.SubElement(structureClass, "registration")
tagEvaluations = ET.SubElement(structureClass, "evaluations")

# Make student records for registration section

## for each entry, run the following to sub in values
## and map data to an attribute
# https://cmdlinetips.com/2018/12/how-to-loop-through-pandas-rows-or-how-to-iterate-over-pandas-rows/
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
    for field in cols:
        fieldName = str(field)
        fieldValue = str(row[fieldName])
        # fieldValueReplaced = str.replace('$', fieldValue)
        print(fieldName)
        if fieldName != fieldName:
            # questionItem.set(fieldName, fieldValue)
            print("test")

    # Make student records for evaluation section
tree = ET.ElementTree(root)
tree.write("data_out/dataout.xml", encoding="utf-8", xml_declaration=True)