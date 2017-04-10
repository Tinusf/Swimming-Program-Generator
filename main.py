import csv
import random

settings = {}
validExerciseList = []

chanceForFins = 10 #% chance
chanceForPaddles = 10 #% chance

# Default settings, you can change these if you want to.
warmUpLength = 400
warmDownLength = 200
settings["crawl"] = True
settings["special"] = True
settings["freestyle"] = True

def testingSettings():
    # Run this function when you are testing instead of running getInput()
    settings["intensity"] = 50
    settings["breastroke"] = True
    settings["backstroke"] = False
    settings["butterfly"] = False
    settings["medley"] = False
    settings["kick"] = True
    settings["longDistancePool"] = False
    settings["paddles"] = True
    settings["fins"] = True

def savePlanTxt():
    # Don't really need this tbh.
    pass

def savePlanSpreadsheet():
    with open("sets/list.csv", "w", newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
        spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

def printPlan():
    pass

def makeExcercisePlan():
    pass

def loadExercises():
    with open("sets/list.csv", newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            formatAndStoreExercises(row)

def formatAndStoreExercises(excercise):
    if (excercise[0] != "Repetitions"): # Filter out the very first line (there probably is a better way to do this.
        # The first 3 should be ints.
        excercise[0] = int(excercise[0])
        excercise[1] = int(excercise[1])
        excercise[2] = int(excercise[2])

        # The last three should be booleans.
        excercise[6] = excercise[6] == "Y"
        excercise[7] = excercise[7] == "Y"
        excercise[8] = excercise[8] == "Y"

        for styles in (excercise[3].split(" ")): # Filter out unwanted swimming styles.
            if not settings[styles]:
                return
        if (settings["longDistancePool"] and not excercise[8]):
            # Filter out impossible exercises because of long distance pools.
            return
        validExerciseList.append(excercise)

def saveSettings():
    pass

def loadSettings():
    pass

def getInput():
    settings["intensity"]= int(input("Intensity (1-100): "))
    settings["breastroke"] = bool(input("Want to swim breaststroke?(Y or N): ").upper() == "Y")
    settings["backstroke"] = bool(input("Want to swim backstroke?(Y or N): ").upper() == "Y")
    settings["butterfly"] = bool(input("Want to swim butterfly?(Y or N): ").upper() == "Y")
    settings["medley"] = bool(input("Want to swim medley?(Y or N): ").upper() == "Y")
    settings["kick"] = bool(input("Want to do kicks?(Y or N): ").upper() == "Y")
    settings["longDistancePool"] = bool(input("Swimming in long distance pool?(Y (50m) or N (25m): ").upper() == "Y")
    settings["paddles"] = bool(input("Want to use paddles?(Y or N): ").upper() == "Y")
    settings["fins"] = bool(input("Want to use fins?(Y or N): ").upper() == "Y")

def main():
    #args = getInput()
    testingSettings()
    loadExercises()
    print(validExerciseList)



main()