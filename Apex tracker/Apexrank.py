import requests
import csv
import datetime
import pandas as pd
import os

def addProfile(player,platform,auth,update=False):
    os.system('cls')
    
    today = datetime.datetime.now()
    rawData = getCurrentRank(player,platform,auth)

    if(rawData == False):
        return()

    data = [player, rawData["rankName"], rawData["rankDiv"], rawData["rankScore"], today, platform]

    if (findprofile(player) == 0):
        with open('profiles.csv', mode ='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)

        if(update == False):
            print("Profile added successfully.")
        else:
            print("New session initialized for " + player + ".")

    else:
        print("Profile already exists please initialize a session instead.")

def compareProfile(player, platform,auth):
    os.system('cls')

    today = datetime.datetime.now()
    rawData = getCurrentRank(player,platform,auth)

    if(rawData == False):
        return()

    newData = [player, rawData["rankName"], rawData["rankDiv"], rawData["rankScore"], today, platform]

    oldData = findprofile(player)
    if (oldData == 0):
        print("Profile not found please add instead.")

    else:
        print("PLAYER STATISTICS")
        print("Username : " + player)
        print("Platform : " + platform)
        print("Rank Change: ")
        print(f"     Net Change = {int(newData[3]) - int(oldData[3])}")

        print("     ", end = "")
        for i in range(1,5):
            print(oldData[i], end = " ")

        print()
        print("                  ˅")
        print("                  ˅")

        print("     ", end = "")
        for i in range(1,5):
            print(newData[i], end = " ")

        print("\n\n\n")

def findprofile(player):
    os.system('cls')

    with open('profiles.csv', mode ='r') as file:
        csvFile = csv.reader(file)

        profiles = []
        for lines in csvFile:
            profiles.append(lines)

    for i in range(len(profiles)):
        if (profiles[i][0] == player):
            return(profiles[i])

    return(0)

def getCurrentRank(player,platform,auth):
    url = "https://api.mozambiquehe.re/bridge?auth=" + auth + "&player=" + player + "&platform=" + platform

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers)

    if(response.text == "Error: API key doesn't exist !"):
        print("API key invalid, please enter a valid key")
        return(False)

    data = response.json()

    if('Error' in data):
        print("Player not found, Please try again.")
        return(False)


    output = {
                'rankScore' : data["global"]["rank"]["rankScore"], 
                'rankName'  : data["global"]["rank"]["rankName"], 
                'rankDiv'   : data["global"]["rank"]["rankDiv"]
             }


    return(output)

def updateProfile(player, platform,auth):
    deleteProfile(player)

    addProfile(player,platform,auth,True)

def deleteProfile(player):
    os.system('cls')
    if(not findprofile(player)):
        print("No such profile has been added, please try again.")
        return()
    
    df = pd.read_csv('profiles.csv')
    df = df[~df.username.isin([player])]
    df.to_csv('profiles.csv', index=False)
    
    print("Profile " + player + " has been successfully deleted.")
