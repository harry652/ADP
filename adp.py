# -*- coding: iso-8859-15 -*-
#
#  adp.py
#  ADP Project
#
#  Created by Stefan Turnau on 23.03.2017.
#  Copyright (c) 2017 Stefan Turnau. All rights reserved.
#

from six.moves.urllib.request import urlopen
import os, sys

startingURL="https://skos.agh.edu.pl"
letterList=[]
letterFindIndex=0
nameList=[]
nameFindIndex=0
nameCount=0
dataTab=[]

mainPage=urlopen(startingURL)
mainPage=mainPage.read()

#tutaj szukamy URL literek, zgodnie ze sposobem podanym na zajęciach
#na wejściu funkcja potrzebuje jedynie punktu startowego
def letterFind(letterStart):
    startingLetterPoint=mainPage.find('https://skos.agh.edu.pl/search/?letter=',letterStart)
    endingLetterPoint=mainPage.find('"',startingLetterPoint)
    letterLink=mainPage[startingLetterPoint:endingLetterPoint]
    return letterLink, endingLetterPoint

#tutaj na wejściu funkcja otrzymuje zawartość strony z listą nazwisk na daną literę
#oprócz tego, całość działa podobnie jak wyżej - też otrzymuje punkt startowy
def nameFind(nameStart, letterPage):
    startingNamePoint=letterPage.find('https://skos.agh.edu.pl/osoba/', nameStart)
    endingNamePoint=letterPage.find('"', startingNamePoint)
    nameLink=letterPage[startingNamePoint:endingNamePoint]
    return nameLink, endingNamePoint

#ta funkcja szuka liczby osób na stronie, wyświetlanej u góry ("Liczba znalezionych osób")
#jest to potrzebne by skutecznie skończyć wyszukiwanie i oszczędzić czasu pracy programu
def countNames(letterPage):
    startingNameCountPoint=letterPage.find('Liczba znalezionych os')
    endingNameCountPoint=letterPage.find('<', startingNameCountPoint)
    nameCount=letterPage[startingNameCountPoint+33:endingNameCountPoint]
    return nameCount
#--------------------------------------------------------------------------------------------
#tego nie trzeba, to już znajduje wszystkie potrzebne dane
class skosName:
    
    def _init_(self):
        self.data=''
    def find(self, className, namePage):
        while True:
            startingClassPoint=namePage.find(className)
            if startingClassPoint==-1:
                break
            endingClassPoint=namepage.find('</a>',startingEntityPoint)
            entity.append(namepage[(startingEntityPoint+len(className)+2):endingEntityPoint])

def findTitle(namePage)

def findName(namePage)

def findEntity(namePage)
    entity=''
    while True
        startingEntityPoint=namePage.find('organisation-name')
        if startingEntityPoint==-1: break
        endingEntityPoint=namepage.find('</a>',startingEntityPoint)
        entity.append(namepage[(startingEntityPoint+19):endingEntityPoint])

    while True:

def findPosition(namePage)

def findGroup(namePage)

def findHQ(namePage)

def findPhone(namePage)

def findMobile(namePage)

def findAdress(namePage)
#--------------------------------------------------------------------------------------------




#ta pętla zapisuje do listy i jednocześnie wypisuje na ekran URL literek
#korzysta ona z funkcji letterFind i jedyne co robi to podaje jej na wejściu to,
#co poprzednio wypluła (czyli endingLetterPoint)
#warunkiem przerwania pętli jest napotkanie ostatniego linku (czyli dla litery ż)
while True:
    letterData=letterFind(letterFindIndex)
    list.append(letterList,letterData[0])
    print("Pobrano link: "+letterData[0])
    if letterData[0]=='https://skos.agh.edu.pl/search/?letter=%C5%BB':
        break
    else:
        letterFindIndex=letterData[1]
        continue

#ta pętla ostatecznie znajduje linki do stron osobowych i zapisuje je do listy, oraz wyświetla na ekran
#na początku sprawdza czy przypadkiem URL nazwiska nie pokrywa się z url dla q, bo z tym był mały problem
#następnie program pobiera zawartość strony z listą nazwisk na daną literę
#przed wejściem w pętlę while - analogiczną do pętli dla wypisywania URL literek - korzysta z funkcji
#countNames, by następna pętla wiedziała ile odliczać
for letterURL in letterList:
    if letterURL=='https://skos.agh.edu.pl/search/?letter=Q':
        list.append(nameList, 'https://skos.agh.edu.pl/osoba/katarzyna-quirini-poplawska-5905.html')
        print("Pobrano link: "+"https://skos.agh.edu.pl/osoba/katarzyna-quirini-poplawska-5905.html")
        continue
    letterPage=urlopen(letterURL)
    letterPage=letterPage.read()
    nameCount+=int(countNames(letterPage))
    print(nameCount)
    while True:
        nameData=nameFind(nameFindIndex, letterPage)
        list.append(nameList, nameData[0])
        print("Pobrano link: "+nameData[0])
        if nameCount<=len(nameList):
            nameFindIndex=0
            break
        else:
            nameFindIndex=nameData[1]
            continue
