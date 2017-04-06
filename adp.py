# -*- coding: iso-8859-15 -*-
#
#  adp.py
#  ADP Project
#
#  Created by Stefan Turnau on 23.03.2017.
#
# =========================================
#
# ogólnie o programie: zamiast pisać kilka funkcji robiących w zasadzie to samo - tak jak na zajęciach
# postanowiłem napisać jedną, która korzysta z listy różnych klas CSS. Dodatkową różnicą, jest skorzystanie
# z drugiego słownika 'pomocniczego', by sensownie nazywać pola w słowniku z danymi, na podstawie nazw klas CSS
#
# ================================================================================

import os, sys, json
from six.moves.urllib.request import urlopen

startingURL = 'https://skos.agh.edu.pl' # url od którego zaczynamy zabawe
letterList = [] # ta lista będzie zawierać url do stron z listą nazwisk na tę samą literę
letterFindIndex = 0 # ta zmienna globalna była potrzebna by wyjść z nią ponad pętlę while - krótko mówiąc, jest to iteracja dla pierwszej pętli
nameList = [] # ta lista będzie zawierać url do stron z danymi osobowymi poszczególnych osób
nameCount = 0 # podobna potrzeba jak przy letterFindIndex - leżąca luźno pętla potrzebowała zmiennej globalnej
dataList = [] # ta tablica będzie zawierała wszystkie dane, przy czym pojedynczy rekord będzie zawierał słownik z danymi danej osoby
# poniższa lista zawiera osobne nazwy słownikowe dla siedziby
siedzibaList=['budynek', 'pietro', 'pokoj']
# poniższa lista zawiera wszystkie możliwe klasy CSS
CSSclasses = ['given-name','family-name','organization-name','organization-unit','class=\"title\"','class=\"tel\"']
# poniższy słownik tłumaczy nazwy klas CSS na nazwy dla słownika danych
dictionaryNames = {'given-name':'imie', 'family-name':'nazwisko', 'organization-name':'jednostka nadrzedna', 'organization-unit':'jednostka',
'class=\"title\"':'stanowisko','class=\"tel\"':'telefon'}

# ================================================================================

mainPage = urlopen(startingURL)
mainPage = mainPage.read()

# tutaj szukamy URL literek, zgodnie ze sposobem podanym na zajęciach
# na wejściu funkcja potrzebuje jedynie punktu startowego
def letterFind(letterStart):
    startingLetterPoint = mainPage.find('https://skos.agh.edu.pl/search/?letter=',letterStart)
    endingLetterPoint = mainPage.find('"',startingLetterPoint)
    letterLink = mainPage[startingLetterPoint:endingLetterPoint]
    return letterLink, endingLetterPoint

# tutaj na wejściu funkcja otrzymuje zawartość strony z listą nazwisk na daną literę
# oprócz tego, całość działa podobnie jak wyżej - też otrzymuje punkt startowy
def nameFind(nameStart, letterPage):
    startingNamePoint = letterPage.find('https://skos.agh.edu.pl/osoba/', nameStart)
    endingNamePoint = letterPage.find('"', startingNamePoint)
    nameLink = letterPage[startingNamePoint:endingNamePoint]
    return nameLink, endingNamePoint

# ta funkcja szuka liczby osób na stronie, wyświetlanej u góry ("Liczba znalezionych osób")
# jest to potrzebne by skutecznie skończyć wyszukiwanie i oszczędzić czasu pracy programu
def countNames(letterPage):
    startingNameCountPoint = letterPage.find('Liczba znalezionych os')
    endingNameCountPoint = letterPage.find('<', startingNameCountPoint)
    nameCount = letterPage[startingNameCountPoint+33:endingNameCountPoint]
    return nameCount

# ta funkcja znajduje wszystkie zawartości dla danej klasy css na stronie z informacjami danej osoby
# na wejściu potrzebujemy className (uzyskane z tablicy CSSclasses) i zawartość strony danej osoby (namePage)
def classFind(className, namePage):
    classReturn = ""
    startingClassPoint = namePage.find(className)
    if startingClassPoint==-1: # w wypadku, gdy nie znajdziemy danej klasy CSS (a to sie zdarza), funkcja zwraca None, czyli null
        return None
    while True:
        startingClassPoint = namePage.find('>', startingClassPoint)
        endingClassPoint = namePage.find('<',startingClassPoint)
        classReturn += namePage[startingClassPoint+1:endingClassPoint]
        startingClassPoint = namePage.find(className,endingClassPoint)
        if startingClassPoint == -1: # warunek przerwania pętli jest dokładnie taki jak na zajęciach: szukamy aż do końca strony
            break
    classReturn += ' / ' #to pozwala na uzyskanie formatu np. tela / telb / telc w przypadku wielu telefonów na stronie
    return classReturn



def siedzibaFind(namePage): #to jest specjalna funkcja dla siedziby, jako że ona nie miała swojej klasy w css
    startingSiedzibaPoint = namePage.find('Siedziba')
    if startingSiedzibaPoint == -1: #warunek tak jak w classFind
        return None
    startingSiedzibaPoint = namePage.find('td', startingSiedzibaPoint)
    startingSiedzibaPoint = namePage.find('>', startingSiedzibaPoint)
    endingSiedzibaPoint = namePage.find('<',startingSiedzibaPoint)
    siedziba = namePage[startingSiedzibaPoint+1:endingSiedzibaPoint]
    siedziba=siedziba.split(',') #dzięki temu, zmienna siedziba dynamicznie się zmienia z vara na tuple i dostajemy krotkę z 3 elementami siedziby, poprzedzielanymi przecinkami
    return siedziba

# ================================================================================

# ta pętla zapisuje do listy i jednocześnie wypisuje na ekran URL literek
# korzysta ona z funkcji letterFind i jedyne co robi to podaje jej na wejściu to,
# co poprzednio wypluła (czyli endingLetterPoint)
# warunkiem przerwania pętli jest napotkanie ostatniego linku (czyli dla litery ż)
while True:
    letterData = letterFind(letterFindIndex)
    list.append(letterList,letterData[0])
    print("Pobrano link: "+letterData[0])
    if letterData[0] == 'https://skos.agh.edu.pl/search/?letter=%C5%BB': # równie dobrze można by kombinować z -1, ale to by obciążyło pętlę
        break
    else:
        letterFindIndex = letterData[1]
        continue #tego nie było na zajęciach chyba; continue powoduje powrót do początku pętli i przestawienie iteracji jeśli taka jest

# ta pętla ostatecznie znajduje linki do stron osobowych i zapisuje je do listy, oraz wyświetla na ekran
# na początku sprawdza czy przypadkiem URL nazwiska nie pokrywa się z url dla q, bo z tym był mały problem
# następnie program pobiera zawartość strony z listą nazwisk na daną literę
# przed wejściem w pętlę while - analogiczną do pętli dla wypisywania URL literek - korzysta z funkcji
# countNames, by następna pętla wiedziała ile odliczać
for letterURL in letterList:
    nameFindIndex = 0
    if letterURL == 'https://skos.agh.edu.pl/search/?letter=Q':
        list.append(nameList, 'https://skos.agh.edu.pl/osoba/katarzyna-quirini-poplawska-5905.html')
        print("Pobrano link: "+"https://skos.agh.edu.pl/osoba/katarzyna-quirini-poplawska-5905.html")
        continue # o tutaj przeskakujemy na początek pętli i przeskakujemy w iteracji letterList
    letterPage = urlopen(letterURL)
    letterPage = letterPage.read()
    nameCount += int(countNames(letterPage)) # int() na wszelki wypadek, bo niby wyszukaliśmy fragment tekstu; to dobry obyczaj tak robić
# co ważne, wyżej liczymy SUMĘ naszych linków, to przyda się potem
    print(nameCount)
    while True:
        nameData = nameFind(nameFindIndex, letterPage) # funkcja nameFind zwraca nameLink i endingNamePoint - czyli krotkę
        list.append(nameList, nameData[0]) # pierwszy (zerowy) element krotki to właśnie link, który ładujemy na stos
        print("Pobrano link: "+nameData[0])
        if nameCount <= len(nameList): #liczymy naszą listę W SUMIE i porównujemy z SUMĄ liczb oznaczających ilość tych gówienek na stronie. to jest  nasz warunek przerwania pętli
            break
        else:
            nameFindIndex = nameData[1] # przepisujemy nameFindIndex do drugiego (pierwszego) elementu krotki
            continue
                                        
# ta pętla wypisuje do słowników wszystkie dane wszystkich osób (słowniki będą zapisywane do listy dataList). Potrójnie zagnieżdżona pętla dla potrójnej radości z rozumienia działania programu.
# pierwsza pętla - odpowiada za pobieranie kolejnych linków do stronek z url i ładowanie ich zawartości do zmiennej namePage
for nameURL in nameList:
    namePage = urlopen(nameURL)
    namePage = namePage.read()
    dataDict = {}
    # druga pętla - odpowiada za pobieranie kolejnych klas CSS z listy i przeszukiwanie wg nich zawartości strony namePage
    for className in CSSclasses:
        classData = classFind(className, namePage)
        if classData is None: #tym sposobem unikamy pustych rekordów w słowniku i zbędnego zajmowania pamięci
            continue
        dataDict[dictionaryNames[className]] = classData
    siedziba = siedzibaFind(namePage)
    if siedziba is not None: # tu podobnie jak wyżej (unikanie pustych rekordów)
        i=0
        # trzecia pętla - odpowiada za przeszukiwanie tablicy z nazwami elementów siedziby (pokój, piętro, budynek) i wprowadzanie ich do słownika wg kolejności ich występowania na SKOS
        for place in siedzibaList:
            dataDict[place] = siedziba[i].strip() #+18
            i += 1
    print(dataDict)
    dataList.append(dataDict)

simplejson = json
dataFile = open("data.txt","w")
simplejson.dump(dataList,dataFile)
dataFile.close()
