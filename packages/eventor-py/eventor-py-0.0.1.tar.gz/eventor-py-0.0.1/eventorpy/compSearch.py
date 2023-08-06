'''
This is a program that based on some parameters searches for orienteering compeitions.
Version: 2020-08-04
Made By: William Grunder
'''

import requests
from xml.etree import ElementTree
import datetime
import os
import errno


def search(KEY, fromDate, toDate, classificationList):
    championchip  = classificationList[0]
    national      = classificationList[1]
    district      = classificationList[2]
    near          = classificationList[3]
    club          = classificationList[4]
    international = classificationList[5]

    url = 'https://eventor.orientering.se/api/events?fromDate=' + fromDate +'&toDate=' + toDate #url for api call
    response = requests.get(url, headers={'ApiKey': KEY}) #api call

    if response.ok:
        root = ElementTree.fromstring(response.content) #Parse response as xml-file

        date = []
        datum = []
        IDs = []
        names = []
        status = []
        everything = []

        for competition in root:
            eventClassificationId = int(competition[2].text)
            eventStatusId = int(competition[3].text)
            disciplineId = int(competition[4].text)

            if classificationList[eventClassificationId - 1] == True: #Sorts out small competitionetitions
                if disciplineId == 1: #Sorts out non-orienteering events
                    date.append(datetime.datetime.strptime(competition[6][0].text, '%Y-%m-%d'))
                    datum.append(competition[6][0].text)
                    IDs.append(competition[0].text)
                    names.append(competition[1].text)

                    st = int(competition[3].text)
                    if st == 1: status.append("Applied")
                    elif st == 2: status.append("ApprovedByRegion")
                    elif st == 3: status.append("Approved")
                    elif st == 4: status.append("Created")
                    elif st == 5: status.append("Entryopened")
                    elif st == 6: status.append("EntryPaused")
                    elif st == 7: status.append("EntryClosed")
                    elif st == 8: status.append("Live")
                    elif st == 9: status.append("Completed")
                    elif st == 10: status.append("Canceled")
                    elif st == 11: status.append("Reported")

        date, datum, IDs, names, status = zip(*sorted(zip(date, datum, IDs, names, status))) #Sort all lists based on date

        everything = [date, datum, IDs, names, status]
        
        return everything
    
    else:
        return response.code