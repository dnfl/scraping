#!/usr/bin
# -*- coding: utf-8 -*-
import bs4, requests, os, time
from mutagen.mp3 import MP3


siteURL = "http://www.laits.utexas.edu/ppp/"
url = "http://www.laits.utexas.edu/ppp/learning.php?unit="


urlList =[]


logfile = "logDLppp.txt"
with open(logfile, 'w') as logLesson:
    logLesson.write("Start\n")

# Script working for lessons 1 to 10
for lessonNumber in range(1, 11):
    unitUrl = url + str(lessonNumber)
    #urlList.append(unitUrl)
    with open(logfile, 'a') as logLesson:
        logLesson.write("Lesson " + str(lessonNumber) +"\n")

    payload = requests.get(unitUrl)
    soup = bs4.BeautifulSoup(payload.content)
    tdList = soup.find_all('td')
    soundsUrlDict = {}


    for i in tdList:
        onclick = i.a["onclick"]
        if "pitch" in onclick:
            soundsUrlDict[i.text + onclick[onclick.index("mp3")-3:onclick.index("mp3")-1] + " pitch"] = siteURL + onclick[onclick.index("audio"):onclick.index("mp3")+3]
        elif "word" in onclick:
            soundsUrlDict[i.text + " word"] = siteURL + onclick[onclick.index("audio"):onclick.index("mp3")+3]

    for soundName in soundsUrlDict.keys():
        #print soundName
        audioFileName = soundName + ".mp3"
        soundData = requests.get(soundsUrlDict[soundName])
        with open(audioFileName, "w") as audioFile:

            for chunk in soundData.iter_content(8192):
                audioFile.write(chunk)

        # Deleting Metadata
        audioTag = MP3(audioFileName)
        audioTag.delete()
        #print(audioTag.pprint())

        with open(logfile, "a") as log:
            if "word" in soundName:
                log.write(soundName.encode("utf-8") + "\n")
            elif "pitch" in soundName:
                log.write(soundName.encode("utf-8") + "\n")

        #
        time.sleep(0.5)
    print "Finished downloading files for lesson " + str(lessonNumber)
    #with open(logfile, 'a') as logLesson:
    logLesson.write("\n\n")
    #time.sleep(5)
