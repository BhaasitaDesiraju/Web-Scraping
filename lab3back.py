#lab3back.py - Bhaasita

# import requests
# from bs4 import BeautifulSoup
import json
import sqlite3

'''getting page contents'''
# page = requests.get("https://en.wikipedia.org/wiki/List_of_most_popular_given_names")
# soup = BeautifulSoup(page.content, "lxml")

'''getting table contents'''
# tableData = soup.find_all("table",{"class":"wikitable"})

# regionDict = {}
# for tag in tableData:
#     descendentData = tag.find_all('tr')  #getting each row
#     for row in descendentData:
#         firstCol = True
#         data = []
#         countryName = ""
#         cols = row.find_all('td')   #getting data of each row
#         for col in cols:
#             if(firstCol):
#                 colStr = col.text
#                 anchor = col.find('a')
#                 if anchor.parent.sup is None :
#                     countryName = colStr
#                 else:
#                     countryName = anchor.text
#                 firstCol = False
#                 if "(" in countryName:
#                     index = countryName.find("(")
#                     countryName = countryName[0:index].strip()
#
#             else:
#                 colData = col.text
#                 if not colData.startswith('NA'):
#                     colData = colData.split(",")
#                     if countryName in regionDict:
#                         data = regionDict[countryName]
#                     else:
#                         regionDict[countryName]= data
#                     data.extend(colData)
#

# with open('data.json', 'w') as fh:
#     json.dump(regionDict, fh)   #dumping the dictionary into a json file

with open('data.json', 'r') as fh:
    jsonData = json.load(fh)    #loading the json file into a json object

sqlite_file = 'regionalDataDB.sqlite'
conn = sqlite3.connect(sqlite_file)   #connecting to a database
cur = conn.cursor()
cur.execute('''DROP TABLE IF EXISTS CommonNames''')
cur.execute('''CREATE TABLE CommonNames(
                   countryName TEXT NOT NULL PRIMARY KEY)''')  #creating a database table
for i in range(100):
    cur.execute('''ALTER  TABLE  CommonNames ADD COLUMN {} TEXT'''.format('name'  +  str(i)))

#insert country name into table
insertPrefix = "INSERT INTO CommonNames(CountryName,"
execString = ""
for countryName in jsonData:
    dataValues = jsonData[countryName]
    colNames = ""
    placeholders = ""
    for i in range(len(dataValues)):
        colNames = colNames + "name" + str(i)
        colValue = dataValues[i]
        if colValue[len(colValue) - 1] == '\n':
            colValue = colValue[:-1]
            dataValues[i] = colValue
        placeholders += "\"" + dataValues[i] + "\""
        if i != len(dataValues)-1:
            colNames += ','
            placeholders += ','
    execString = insertPrefix + colNames + ") VALUES (\"" + countryName + "\"," + placeholders + ")"
    print(execString)
    cur.execute(execString)

conn.commit()
conn.close()
