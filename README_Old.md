# Developer Information

## Choose the 3 files

### Pre-requisites for files:

- Save all data files as .csv format, comma-separated, with Latin ISO/IEC 8859-1
  encoding

### Pre-processing required for LMS/Roster data:

- Pre-filter the student data records via the LMS data output OR manually remove
  non-relevant student records before using RESonator
- Manually remove the instructors' records from the LMS data

### Evaluation Data (from ZipGrade):

- Do not change any field names

### Metadata

Copy the metadata template file and

- Ensure date/times are in MMDDYYYY format
- Save with Latin ISO/IEC 8859-1 encoding

## Click "Compile XML" to begin the XML compilation process

- Manually adjust the final sequence number from "n" to the desired number.
- Date is automatically filled to the current date/time
- RESonator will overwrite an existing file with the same name
- XML outputs to the user's home folder

## RESonator Developer's Guide

RESonator is a tool for preparing course data for input to the FEMA RES system.

RESonator takes in three CSV files:

- Data representing student registration from the LMS system
- Data representing student evaluations
- A hand-prepared file representing metadata on the course, instructor, and test
  averages.

## Major issues

### DOCTYPE cannot be inserted through ElementTree

Seems like the DOCTYPE must be inserted by hand after the XML declaration?

`<!DOCTYPE Manifest SYSTEM "submission.dtd">`

Notes: This script uses Python 3.7,
[see lang references ](https://docs.python.org/3/) This Python script reads in a
data file and outputs it to a XML file

## Resources for Python

[Using for loops](https://docs.python.org/3/reference/compound_stmts.html#the-for-statement)

[Defining functions in Python](https://docs.python.org/3/reference/compound_stmts.html#function-definitions)

[Pandas API reference](https://pandas.pydata.org/pandas-docs/stable/reference/index.html)

## data manip tasks/formatting

[Series.str.strip for removing symbols which seems to botch stuff](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.strip.html)

[Casting datatypes in dataframes](https://stackoverflow.com/questions/37697934/how-to-remove-symbol-for-particular-column-in-dataframeusing-python-pandas)

## XML-specific Stuff

[API Docs for ElementTree](https://docs.python.org/3/library/xml.etree.elementtree.html)

# Scratch

[Apply pandas functions](https://realpython.com/fast-flexible-pandas/#pandas-apply)

https://towardsdatascience.com/the-easy-way-to-work-with-csv-json-and-xml-in-python-5056f9325ca9

https://stackoverflow.com/questions/18574108/how-do-convert-a-pandas-dataframe-to-xml
