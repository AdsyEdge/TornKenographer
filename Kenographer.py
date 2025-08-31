import json
import os
import time
import datetime
from datetime import date, timedelta
import calendar as cal
try:
    import requests
    import matplotlib.pyplot as plt
    import numpy as np
except:
    print("Installing required modules (REQUESTS, NUMPY, and MATPLOTLIB).\n\
These modules allow the script to fetch JSON data and arrange it in graphs.\n\
This script doesn't function without these modules.\n\
If you don't want these modules to be installed, stop this script and delete this file.")
    scriptInstallCounter = 31
    for i in range(31):
        scriptInstallCounter -= 1
        print('This script will install in %d seconds' % scriptInstallCounter, end='\r')
        time.sleep(1)
    os.system("py -m pip install pip")
    os.system("py -m pip install requests")
    os.system("py -m pip install numpy")
    os.system("py -m pip install matplotlib")
    import requests
    import matplotlib.pyplot as plt
    import numpy as np
    print("\n\n\n\n\n")

TitleLogo = \
 "░█░█░█▀▀░█▀█░█▀█░█▀▀░█▀▄░█▀█░█▀█░█░█░█▀▀░█▀▄\
\n░█▀▄░█▀▀░█░█░█░█░█░█░█▀▄░█▀█░█▀▀░█▀█░█▀▀░█▀▄\
\n░▀░▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀░▀░▀░▀░▀░░░▀░▀░▀▀▀░▀░▀"
print(TitleLogo)

# IMPORTANT INFO, PLEASE READ
# DATA STORAGE - If selected in menu options, .JSON files of imported log files are stored locally
# DATA SHARING - Nobody else can access the data processed through this script
# PURPOSE OF USE - The purpose of use is for non-malicious statistical analysis
# KEY STORAGE & SHARING - The API key is not stored or shared
# KEY ACCESS - Due to the need of accessing user logs, this script needs either a Full Access key, or a custom key with access to basic user data & user logs

def getTornKeyAPI():
    tornKeyAPIFinish = False
    while tornKeyAPIFinish == False:
        # Gets data about given API Key
        tornKeyAPI = input("Please enter your Torn API: ")
        APIURL = ("https://api.torn.com/v2/user/basic?striptags=true&key=" + tornKeyAPI)
        APIJSON = requests.get(APIURL)
        TornAPIData = APIJSON.json()
        try:
            # Prints fancy loading text
            print('.', end='\r'), time.sleep(.2), print('. .', end='\r'), time.sleep(.2), print('. . .', end='\r'), time.sleep(.4), print('     ', end='\r'), time.sleep(.05)
            print('.', end='\r'), time.sleep(.2), print('. .', end='\r'), time.sleep(.2), print('. . .', end='\r'), time.sleep(.4), print('     ', end='\r'), time.sleep(.05)
            print('.', end='\r'), time.sleep(.2), print('. .', end='\r'), time.sleep(.2), print('. . .', end='\r'), time.sleep(.4)
            # Checks if the given API is valid, by checking if "profile" is in TornAPIData
            if "profile" in TornAPIData:
                # Assets "id" and "name" to values.
                TornID = TornAPIData["profile"].get("id", 0)
                tornName = TornAPIData["profile"].get("name", 0)
                # Checks what fields the API key can access, and verifies if it can access user log data
                VERIFYAPI = ("https://api.torn.com/v2/key?selections=info&limit=100&key=" + tornKeyAPI)
                APIJSONVERIFY = requests.get(VERIFYAPI)
                TornAPIVerify = APIJSONVERIFY.json()
                if "info" in TornAPIVerify:
                    tornAPIAccess = TornAPIVerify["info"].get("access", 0)
                    tornAPISelections = TornAPIVerify["info"].get("selections", 0)
                    tornAPIUserLogAccessLevel = tornAPISelections["user"]
                    if "log" in tornAPIUserLogAccessLevel:
                        print("\n\nAPI Key access level: " + str(tornAPIAccess["type"]).upper() + "\nWelcome, " + str(tornName) + " [" + str(TornID) + "]")
                        tornKeyAPIFinish = True
                    else:
                        print("API key access level not high enough.\nThis key is: " + str(tornAPIAccess["type"]).upper())
                        time.sleep(1)
                        print("\nYou either need:")
                        time.sleep(1)
                        print("   A) a FULL ACCESS API key, or")
                        time.sleep(1)
                        print("   B) a Custom API KEY with access to basic user data & user logs\n")
            else:
                print("API couldn't be verified with Torn, or doesn't have access to basic user data. Online Log access unavailable. Please try again!\n")
            time.sleep(2)
        except:
            print("API Input Error. Please try again.\n")
    return tornKeyAPI


# function to fetch data from Torn's API for Keno category.
def fetchData(unixTimeStart, unixTimeEnd, tornKeyAPI, saveLocalData, loadLocalData, saveDataValue, JSONFileName, JSONFileNameDataFileList, JSONFileDirectory):
    saveDataValue += 1
    if loadLocalData == True:
        JSONFileNameLoad = str(JSONFileName) + "_" +(str(saveDataValue) + ".json")
        JSONFileDirectoryLoad = str(os.getcwd())
        JSONFileFullDirectoryLoad = os.path.join(str(JSONFileDirectoryLoad), str(JSONFileName), str(JSONFileNameLoad))
        with open(JSONFileFullDirectoryLoad, mode="r", encoding="utf-8") as readFile:
            kenoData = json.load(readFile)
    else:
        # V1API
        # APIURL = ("https://api.torn.com/user/?selections=log&cat=188&from=" + str(unixTimeStart) + "&to=" + str(unixTimeEnd) + "&key=" + tornKeyAPI)
        # V2 API
        KENOAPIURL = ("https://api.torn.com/v2/user/log?log=8320,8321&from=" + str(unixTimeStart) + "&to=" + str(unixTimeEnd) + "&key=" + tornKeyAPI)
        # Sleeps for 0.7 seconds, to comply with TORN API regulations of accessing the API no more than 100 times a minute.
        # I chose 0.7 instead of 0.6, to allow for any leeway of other scripts accessing the user's API
        time.sleep(0.7)
        r = requests.get(KENOAPIURL)
        kenoData = r.json()
    
    # Writes logs to file, if option was selected in main menu.
    try:
        if saveLocalData == True:
            if not os.path.isdir(str(JSONFileDirectory)):
                os.mkdir(str(JSONFileDirectory))
            JSONFileNameSave = str(JSONFileName) + "_" +(str(saveDataValue) + ".json")
            JSONFileDirectorySave = ("./" + str(JSONFileDirectory) + "/" + (str(JSONFileNameSave)))
            with open(str(JSONFileDirectorySave), mode="w", encoding="utf-8") as writeFile:
                json.dump(kenoData, writeFile)
            JSONFileNameDataFileList.append(JSONFileNameSave)
    except:
        print("\n\nWRITE ERROR!")
    return kenoData, saveDataValue, JSONFileNameDataFileList



# function to calculate each log entry from the data, parsing a dictionary, a Unix timestamp, and an integer of the logs counted.
def calculateKeno(kenoData, unixTimeEnd, logCount, isRestarted, kenoWinDictionary, kenoMoneyWonDictonary):
    # Initial API fetch
    if isRestarted == True:
        numbersBet = 0
        numbersMatched = 0
        kenoTemp = []
        moneyWonTemp = 0
        moneyWon = []
        logCount = 0
    try:
        # V2 API - Return empty data
        if kenoData["log"] == []:
            return logCount, kenoWinDictionary, kenoMoneyWonDictonary, "stop"
        
        # V1 API - Read log data
        # for entry in data["log"].values():
            # log = entry["log"]
            # unixTimeEnd = entry["timestamp"]

        # V2 API - Read log data
        for entry in kenoData["log"]:
            log = entry["details"]
            unixTimeEnd = entry["timestamp"]
            
            # V1 API - Verify Won Log
            # if "8320" in str(log):

            # V2 API - Verify Won Log
            if "8320" in str(log["id"]):
            
                # Win log
                # Reads the log entry, checks the log type, then gets the bet & matched numbers
                # Matched & Bet are then added to dictionary, and log count is increased by 1
                numbersBet = entry["data"].get("numbers", 0)
                numbersMatched = entry["data"].get("matches", 0)
                kenoTemp = kenoWinDictionary[numbersBet]
                kenoTemp[numbersMatched] += 1
                betAmount = entry["data"].get("bet_amount", 0)
                moneyWonTemp = entry["data"].get("won_amount", 0)
                moneyWon = kenoMoneyWonDictonary[numbersBet]
                moneyWon[numbersMatched] += (moneyWonTemp - betAmount)
                logCount += 1

            # V1 API - Verify Lost Log
            # elif "8321" in str(log):

            # V2 API - Verify Lost Log
            if "8321" in str(log["id"]):
            
                # Lose log
                # Reads the log entry, checks the log type, then gets the bet & matched numbers
                # Matched & Bet are then added to dictionary, and log count is increased by 1
                numbersBet = entry["data"].get("numbers", 0)
                numbersMatched = entry["data"].get("matches", 0)
                kenoTemp = kenoWinDictionary[numbersBet]
                kenoTemp[numbersMatched] += 1
                moneyWonTemp = entry["data"].get("bet_amount", 0)
                moneyWon = kenoMoneyWonDictonary[numbersBet]
                moneyWon[numbersMatched] -= moneyWonTemp
                logCount += 1
            print('Logs read: %d' % logCount, end='\r')
    except:
        return logCount, kenoWinDictionary, kenoMoneyWonDictonary, "Stop"
    return  logCount, kenoWinDictionary, kenoMoneyWonDictonary, unixTimeEnd



def MainScript(tornKeyAPI, saveLocalData, loadLocalData):
    # Fetches Main Menu function, to get 3 Unix timestamps
    mainMenuData = mainMenu(saveLocalData, loadLocalData)
    unixTimeStart = mainMenuData[0]
    unixTimeEnd = mainMenuData[1]
    JSONFileNameData = mainMenuData[2]
    JSONFileDirectory = JSONFileNameData
    saveLocalData = mainMenuData[3]
    loadLocalData = mainMenuData[4]
    saveDataValue = 0
    JSONFileNameDataFileList = []


    # Resets the Dictionaries, Log Count & the "looped back verifier"
    logCount = 0
    kenoNumbersPlacedDictonary={1:["0", "1"],
                        2:["0", "1", "2"],
                        3:["0", "1", "2", "3"],
                        4:["0", "1", "2", "3", "4"],
                        5:["0", "1", "2", "3", "4", "5"],
                        6:["0", "1", "2", "3", "4", "5", "6"],
                        7:["0", "1", "2", "3", "4", "5", "6", "7"],
                        8:["0", "1", "2", "3", "4", "5", "6", "7", "8"],
                        9:["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                        10:["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]}
    kenoMoneyWonDictonary={1:[0, 0],
                        2:[0, 0, 0],
                        3:[0, 0, 0, 0],
                        4:[0, 0, 0, 0, 0],
                        5:[0, 0, 0, 0, 0, 0],
                        6:[0, 0, 0, 0, 0, 0, 0],
                        7:[0, 0, 0, 0, 0, 0, 0, 0],
                        8:[0, 0, 0, 0, 0, 0, 0, 0, 0],
                        9:[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        10:[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
    kenoWinDictionary = {1:[0, 0],
                        2:[0, 0, 0],
                        3:[0, 0, 0, 0],
                        4:[0, 0, 0, 0, 0],
                        5:[0, 0, 0, 0, 0, 0],
                        6:[0, 0, 0, 0, 0, 0, 0],
                        7:[0, 0, 0, 0, 0, 0, 0, 0],
                        8:[0, 0, 0, 0, 0, 0, 0, 0, 0],
                        9:[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        10:[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
    isRestarted = True
    firstAPIFetch = True

    # A 'while' loop that keeps looping until the Keno calculator returns a 0 for unixTimeEnd
    while unixTimeEnd != "stop":
        # Fetches next set of data from API, from oldest available UNIX timestamp.
        if firstAPIFetch == True and loadLocalData == False:
            print("\nFETCHING API, PLEASE WAIT...")
        kenoDataTemp = fetchData(unixTimeStart, unixTimeEnd, tornKeyAPI, saveLocalData, loadLocalData, saveDataValue, JSONFileNameData, JSONFileNameDataFileList, JSONFileDirectory)
        if firstAPIFetch == True and loadLocalData == False:
            print("API FETCHED, READING LOGS...")
            firstAPIFetch = False
        kenoData = kenoDataTemp[0]
        saveDataValue = kenoDataTemp[1]
        JSONFileNameDataFileList = kenoDataTemp[2]

        # calculates the data, timestamp & logs counted from function, and parses to 4 separate variables.
        tempValueHolder = calculateKeno(kenoData, unixTimeEnd, logCount, isRestarted, kenoWinDictionary, kenoMoneyWonDictonary)
        isRestarted = False
        logCount = tempValueHolder[0]
        kenoWinDictonary = tempValueHolder[1]
        kenoMoneyWonDictonary = tempValueHolder[2]
        unixTimeEnd = tempValueHolder[3]
    print(str(logCount) + " total logs read.\n\n")

    # If JSON data saved to file, this prints out what files have been saved.
    if logCount > 0:
        if saveLocalData == True and loadLocalData == False:
            JSONFileNameDataFileListPrint = ""
            printLineCount = 0
            for i in range(len(JSONFileNameDataFileList)):
                printLineCount += 1
                JSONFileNameDataFileListPrint = JSONFileNameDataFileListPrint + str(JSONFileNameDataFileList[i])
                if len(JSONFileNameDataFileList) > 1:
                    if i+1 == len(JSONFileNameDataFileList) - 1:
                        JSONFileNameDataFileListPrint = JSONFileNameDataFileListPrint + ", and "
                    elif i+1 < len(JSONFileNameDataFileList):
                        JSONFileNameDataFileListPrint = JSONFileNameDataFileListPrint + ", "
                    if printLineCount == 5:
                        printLineCount = 0
                        JSONFileNameDataFileListPrint = JSONFileNameDataFileListPrint + "\n"
            print(JSONFileNameDataFileListPrint + " has been saved to:\n" + str(os.path.dirname(__file__)) + "\\" + str(JSONFileDirectory))

    # Calls for the menu to access processed data
    return graphMenu(kenoNumbersPlacedDictonary, kenoWinDictonary, kenoMoneyWonDictonary, tornKeyAPI, saveLocalData)
    




def mainMenu(saveLocalData, loadLocalData):
    MainMenuFinished = False
    while MainMenuFinished == False:
        # Prompt user for input
        print("\nWhat would you like to do/what date would you like to read?\n 1 - TODAY" \
        "\n 2 - YESTERDAY\n 3 - MONTH (TO DATE)\n " \
        "4 - YEAR (TO DATE)\n 5 - ALL TIME\n " \
        "6 - CUSTOM DATE\n 7 - CUSTOM RANGE\n " \
        "8 - SAVE TO FILE\n 9 - LOAD FROM FILE\n 0 - EXIT")
        MainMenuInput = input("-> ")
        print("")
        if MainMenuInput == "1" or MainMenuInput.upper() == "TODAY":
            todayValue = date.today()
            year = int(todayValue.strftime("%Y"))
            month = int(todayValue.strftime("%m"))
            day = int(todayValue.strftime("%d"))
            # Calculate start and end times for today
            dateTimeStart = datetime.datetime(year, month, day, 0, 0)
            dateTimeEnd = datetime.datetime(year, month, day, 23, 59, 59)
            MainMenuFinished = True
        elif MainMenuInput == "2" or MainMenuInput.upper() == "YESTERDAY":
            yesterdayValue = date.today() - timedelta(1)
            year = int(yesterdayValue.strftime("%Y"))
            month = int(yesterdayValue.strftime("%m"))
            day = int(yesterdayValue.strftime("%d"))
            # Calculate start and end times for yesterday
            dateTimeStart = datetime.datetime(year, month, day, 0, 0)
            dateTimeEnd = datetime.datetime(year, month, day, 23, 59, 59)
            MainMenuFinished = True
        elif MainMenuInput == "3" or MainMenuInput.upper() == "MONTH (TO DATE)":
            monthValue = date.today()
            year = int(monthValue.strftime("%Y"))
            month = int(monthValue.strftime("%m"))
            day = int(monthValue.strftime("%d"))
            # Calculate start and end times for this month
            dateTimeStart = datetime.datetime(year, month, 1, 0, 0)
            dateTimeEnd = datetime.datetime(year, month, day, 23, 59, 59)
            MainMenuFinished = True
        elif MainMenuInput == "4" or MainMenuInput.upper() == "YEAR (TO DATE)":
            yearValue = date.today()
            year = int(yearValue.strftime("%Y"))
            month = int(yearValue.strftime("%m"))
            day = int(yearValue.strftime("%d"))
            # Calculate start and end times for this year
            dateTimeStart = datetime.datetime(year, 1, 1, 0, 0)
            dateTimeEnd = datetime.datetime(year, month, day, 23, 59, 59)
            MainMenuFinished = True
        elif MainMenuInput == "5" or MainMenuInput.upper() == "ALL TIME":
            todayValue = date.today()
            year = int(todayValue.strftime("%Y"))
            month = int(todayValue.strftime("%m"))
            day = int(todayValue.strftime("%d"))
            # Calculate start and end times for all time
            dateTimeStart = datetime.datetime(2004, 1, 1, 0, 0)
            dateTimeEnd = datetime.datetime(year, month, day, 23, 59, 59)
            MainMenuFinished = True
        elif MainMenuInput == "6" or MainMenuInput.upper() == "CUSTOM DATE":
            try:
                day = int(input("Day: "))
                month = int(input("Month: "))
                year = int(input("Year: "))
            except ValueError as e: print("\nERROR!", e, "\n")          
            # Calculate start and end times for a specific date
            dateTimeStart = datetime.datetime(year, month, day, 0, 0)
            dateTimeEnd = datetime.datetime(year, month, day, 23, 59, 59)
            MainMenuFinished = True    
        elif MainMenuInput == "7":
            submenuFinished = False
            while submenuFinished == False:
                # Submenu to verify that the starting date isn't newer than the ending date.
                try:
                    monthFinish = False
                    yearFinish = False
                    while yearFinish == False:
                        yearStart = int(input("Starting Year: "))
                        yearEnd = int(input("Ending Year: "))
                        if yearEnd >= yearStart:
                            yearFinish = True
                        else:
                            print("INVALID DATE! Ending year cannot be larger than starting year!\n")
                    while monthFinish == False:
                        monthStart = int(input("Starting Month: "))
                        monthEnd = int(input("Ending Month: "))
                        if monthEnd >= monthStart:
                            monthFinish = True
                        elif monthEnd < monthStart & yearEnd > yearStart:
                            monthFinish = True
                        else:
                            print("INVALID DATE! Ending month cannot be larger than starting month!\n")
                    dayStart = int(input("Starting Day: "))
                    dayEnd = int(input("Ending Day: "))
                    if dayEnd > dayStart:
                        submenuFinished = True
                    elif monthEnd > monthStart:
                        submenuFinished = True
                    elif yearEnd > yearStart:
                        submenuFinished = True
                    else:
                        monthFinish = False
                        yearFinish = False
                        print("INVALID DATE! Ending date cannot be larger than starting date!\n")
                    # Calculate start and end times for a specific date
                    dateTimeStart = datetime.datetime(yearStart, monthStart, dayStart, 0, 0)
                    dateTimeEnd = datetime.datetime(yearEnd, monthEnd, dayEnd, 23, 59, 59)
                    MainMenuFinished = True
                except ValueError as e:
                    print("\nERROR!", e, "\n")
                    submenuFinished = False
        elif MainMenuInput == "8":
            # Gets users confirmation or denial for saving data to .json file
            submenuFinished = False
            while submenuFinished == False:
                storeDataInput = input("DO YOU WANT TO STORE API DATA TO FILE? (Y/N) >>")
                if storeDataInput.upper() == "Y" or storeDataInput.upper() == "YES":
                    print("API DATA WILL BE STORED TO FILE, FILENAME WILL BE PRINTED AT END OF CALCULATION")
                    saveLocalData = True
                    submenuFinished = True
                elif storeDataInput.upper() == "N" or storeDataInput.upper() == "NO":
                    print("API DATA WILL NOT BE STORED TO FILE")
                    saveLocalData = False
                    submenuFinished = True
                else:
                    print("REQUEST NOT FOUND! PLEASE TRY AGAIN.")
                time.sleep(1)
            print()
        elif MainMenuInput == "9":
            # Loads .json directory from a user-given UNIX timestamp, if exists
            submenuFinished = False
            while submenuFinished == False:
                loadLocalDataInput = input("Please enter the UNIX timestamp of the JSON data files you want to load (excluding the _# on the end): ")
                loadLocalData = os.path.isfile(str(loadLocalDataInput) + "/" + str(loadLocalDataInput) + "_1.json")
                if loadLocalData == True:
                    print("FILE FOUND! LOADING...\n")
                    time.sleep(1.5)
                    JSONFileNameData = loadLocalDataInput
                    dateTimeStart = 0
                    dateTimeEnd = 0
                    if saveLocalData == True:
                        saveLocalData = 1
                    submenuFinished = True
                    MainMenuFinished = True
                else:
                    print("FILE NOT FOUND! PLEASE TRY LATER.\n")
                    time.sleep(1.5)
                    submenuFinished = True
        elif MainMenuInput == "0":
            # Quits code
            exit()
        else:
            print("REQUEST NOT FOUND! PLEASE TRY AGAIN.\n")
            time.sleep(1)
    if MainMenuInput != "9":
        unixTimeStart = cal.timegm(dateTimeStart.timetuple())
        unixTimeEnd = cal.timegm(dateTimeEnd.timetuple())
        JSONFileNameData = cal.timegm(datetime.datetime.now().timetuple())
    else:
        unixTimeStart = dateTimeStart
        unixTimeEnd = dateTimeEnd
    return unixTimeStart, unixTimeEnd, JSONFileNameData, saveLocalData, loadLocalData



def graphMenu(kenoNumbersPlacedDictonary, kenoWinDictonary, kenoMoneyWonDictonary, tornKeyAPI, saveLocalData):
    numbersBetMenu = False 
    while not numbersBetMenu:
        numbersBetMenuInput = input("\nWhat numbers bet line do you want to see (1-10)?\nTo go back to the main menu, enter 'RESTART'\nTo end script, enter 'END'\n>> ")
        if numbersBetMenuInput.upper() == "END":
            exit()
        elif numbersBetMenuInput.upper() == "RESTART":
            return tornKeyAPI, saveLocalData
        else:
            try:
                # Sets the X & Y axis for the graph, for the betting numbers & numbers placed
                netTotal = 0
                KenoXAxis = np.array(kenoNumbersPlacedDictonary[int(numbersBetMenuInput)])
                KenoYAxis = np.array(kenoWinDictonary[int(numbersBetMenuInput)])
                # If there's only 0s in the array, it parses to below, and states that there's no logs found
                checkKenoListLength = [i for i in KenoYAxis if i != 0]
                if len(checkKenoListLength) > 0:
                    # Sets the labels on the bars
                    for i in range(len(KenoXAxis)):
                        plt.text(i, KenoYAxis[i], KenoYAxis[i], ha="center")
                    plt.xlabel("Numbers Placed")
                    plt.ylabel("Amount")
                    plt.bar(KenoXAxis,KenoYAxis)
                    plt.show()

                    # Sets the Y axis for the Money won/lost
                    KenoYAxis = np.array(kenoMoneyWonDictonary[int(numbersBetMenuInput)])
                    # Calculates each bar, and changes the label if it's a positive or negative value
                    for i in range(len(KenoXAxis)):
                        netTotal += int(KenoYAxis[i])
                        if KenoYAxis[i] >= 0:
                            plt.text(i, KenoYAxis[i], str("${:,}".format(KenoYAxis[i])), ha="center")
                        else:
                            plt.text(i, KenoYAxis[i], str("-${:,}".format(-KenoYAxis[i])), ha="center")
                    plt.xlabel("Numbers Placed")
                    plt.ylabel("Winnings")
                    plt.bar(KenoXAxis,KenoYAxis)

                    # Prints the Overall Net total
                    if netTotal >= 0:
                        print("Overall Net Total: ${:,}".format(netTotal))
                    else:
                        print("Overall Net Total: -${:,}".format(-netTotal))
                    plt.show()

                    # Prints text-accessible data into the command window
                    print("\nText-accessible format:")
                    print("Available numbers:", kenoNumbersPlacedDictonary[int(numbersBetMenuInput)])
                    print("Net Gain/Loss:", kenoMoneyWonDictonary[int(numbersBetMenuInput)])
                    print("Numbers Placed:", kenoWinDictonary[int(numbersBetMenuInput)])
                    time.sleep(1.5)
                else:
                    print("\nNo logs found for this bet type")
                    time.sleep(1.5)
            except:
                print("\nAN ERROR OCCURRED! PLEASE TRY AGAIN.")
                time.sleep(1.5)


endScript = False
while endScript == False:
    loadLocalData = False
    # If API Key doesn't exist, it runs the function to get a API Key.
    try:
        tornKeyAPI
    except NameError:
        tornKeyAPI = getTornKeyAPI()
    # This checks if the "User wants to save JSON data" option has been selected. If it has, great! If not, it sets it to False. The "1" checker is if both load & save data was selected (If both was selected, it sets "save" to 1, so it doesn't save the already saved data twice.) 
    try:
        saveLocalData
        if saveLocalData == 1:
            saveLocalData = True
    except:
        saveLocalData = False
    MainScriptReturn = MainScript(tornKeyAPI, saveLocalData, loadLocalData)
    tornKeyAPI = MainScriptReturn[0]
    saveLocalData = MainScriptReturn[1]
    print("\n\n\n\n")