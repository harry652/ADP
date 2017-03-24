#
#  adp.py
#  ADP Project
#
#  Created by Stefan Turnau on 23.03.2017.
#  Copyright (c) 2017 Stefan Turnau. All rights reserved.
#

from six.moves.urllib.request import urlopen

startingURL="https://skos.agh.edu.pl"
letterList=[]
letterFindIndex=0
nameList=[]
nameFindIndex=0
nameCount=0

mainPage=urlopen(startingURL)
mainPage=mainPage.read()

def letterFind(letterStart):
    startingLetterPoint=mainPage.find('https://skos.agh.edu.pl/search/?letter=',letterStart)
    endingLetterPoint=mainPage.find('"',startingLetterPoint)
    letterLink=mainPage[startingLetterPoint:endingLetterPoint]
    return letterLink, endingLetterPoint

while True:
    letterData=letterFind(letterFindIndex)
    list.append(letterList,letterData[0])
    print("Pobrano link: "+letterData[0])
    if letterData[0]=='https://skos.agh.edu.pl/search/?letter=%C5%BB':
        break
    else:
        letterFindIndex=letterData[1]
        continue

def nameFind(nameStart, letterPage):
    startingNamePoint=letterPage.find('https://skos.agh.edu.pl/osoba/', nameStart)
    endingNamePoint=letterPage.find('"', startingNamePoint)
    nameLink=letterPage[startingNamePoint:endingNamePoint]
    return nameLink, endingNamePoint

def countNames(letterPage):
    startingNameCountPoint=letterPage.find('Liczba znalezionych os')
    endingNameCountPoint=letterPage.find('<', startingNameCountPoint)
    nameCount=letterPage[startingNameCountPoint+33:endingNameCountPoint]
    return nameCount

for letterURL in letterList:
    if letterURL=='https://skos.agh.edu.pl/search/?letter=Q':
        list.append(nameList, 'https://skos.agh.edu.pl/osoba/katarzyna-quirini-poplawska-5905.html')
        print("Pobrano link:"+"https://skos.agh.edu.pl/osoba/katarzyna-quirini-poplawska-5905.html")
        continue
    letterPage=urlopen(letterURL)
    letterPage=letterPage.read()
    nameCount+=int(countNames(letterPage))
    print(nameCount)
    while True:
        nameData=nameFind(nameFindIndex, letterPage)
        list.append(nameList, nameData[0])
        print("Pobrano link:"+nameData[0])
        if nameCount<=len(nameList):
            nameFindIndex=0
            break
        else:
            nameFindIndex=nameData[1]
            continue
