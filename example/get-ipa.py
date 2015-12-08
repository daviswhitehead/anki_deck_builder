# -*- coding: utf-8 -*-

import csv
import json 
import urllib.request
import urllib.parse
import sys

#TODO: Fix limit, select a single database and use that instead.
API = "http://api.wordnik.com/v4/word.json/{0}/pronunciations?api_key={1}&limit=6"

token = "a2a73e7b926c924fad7001ca3111acd55af2ffabf50eb4ae5"

def getPronunciation(word):
    url = API.format(word, token)

    #TODO: URL encoding
    #test = getPronunciation("blas\'e") #Debugging a problem
    #url = urllib.parse.quote_plus(url)

    try:
        with urllib.request.urlopen(url) as loader:
            s = loader.read()
    except:
        return "ERROR obtaining data"

    print(word)


    decoded = s.decode('utf-8')
    data = json.loads(decoded)

    if not data:
        return "No data available"

    return data[0]['raw']



with open('wordlist.txt', 'rt') as csvfile:

    spamreader = csv.reader(csvfile, delimiter=',')
    previous = []
    pronunciations = []
    v = open("ipalist.txt", "ab")

    try:
        for row in spamreader:
            previous.append(row)
            pronunciation = getPronunciation(row[0])
            pronunciations.append(pronunciation)
            encodedToWrite = (pronunciation + '\n').encode('utf-8')
            v.write(encodedToWrite)

    finally:
        #if we hit an error, write what we already have.
        v.close()
        final = open("final.txt", "wb")

        for i in range(0, len(previous)):
            original = previous[i]
            #TODO: Quote escaping
            str = "{0},\"{1}\",\"{2}\"\n".format(original[0], original[1], pronunciations[i])
            final.write(str.encode('utf-8'))

        final.close()