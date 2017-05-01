import csv
import random
import pickle
import os

settings = {}

# Default settings, you can change these if you want to.
chanceForFins = 10 #% chance
chanceForPaddles = 10 #% chance

longDistanceLimit = 200 # How long until it's considered long distance
deltaLimit = 300 # How many less meters is ok.

warmUpExercise = [1, 400, 0, "freestyle", "Warm up", "05:00"]
warmDownExercise = [1, 200, 0, "freestyle", "Warm down", "05:00"]
hundredEZ = [1, 100, 0, "freestyle", "EZ", "05:00"]

settings["crawl"] = True
settings["special"] = True
settings["freestyle"] = True

def savePlanSpreadsheet(plan, length, fileName):
    with open("outputPlans/" + fileName + ".csv", "w", newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Reps', 'Dist', 'Intensity', 'Style(s)', 'Description', 'Start time / Pause'])
        for exercise in plan:
            print(exercise)
            spamwriter.writerow(exercise)
        spamwriter.writerow(['', '', '', '', 'Total exercise length: ' + str(length)])
    print("Saved your plan at outputPlans/" + fileName + ".csv")
    csvfile.close()

def makeExcercisePlan(validPlans):
    currentPlan = []
    totalLength = 0

    currentPlan.append(warmUpExercise)
    totalLength += warmUpExercise[0] * warmUpExercise[1]
    while totalLength < settings["targetLength"] - deltaLimit:
        curRNG = random.randint(0, len(validPlans) -1)
        curExercise = validPlans[curRNG]
        curLength = (curExercise[0] * curExercise[1])
        if (totalLength + curLength) < settings["targetLength"]:
            curExerciseFormat = formatDescription(curExercise)
            currentPlan.append(curExerciseFormat)
            totalLength += curLength
            if (curExerciseFormat[2] >= 75): # If high intensity
                currentPlan.append(hundredEZ)
                totalLength += hundredEZ[1]
        del validPlans[curRNG] # Delete it in both cases: impossible to do and added in the plan.

        if (len(validPlans) < 1):
            print("Not enough plans to add more exercises.")
            break
    totalLength += warmDownExercise[0] * warmDownExercise[1]
    currentPlan.append(warmDownExercise)
    return currentPlan, totalLength

def formatDescription(exercise):
    exercise[4] = str(exercise[0]) + " * " + str(exercise[1]) + " " + exercise[4]
    if settings["paddles"] and exercise[7]:
        if chanceForPaddles >= random.randint(1, 100):
            exercise[4] += ", with paddles"

    if (settings["fins"] and exercise[6]):
        if chanceForFins >= random.randint(1, 100):
            exercise[4] += ", with fins"

    del exercise[7]
    del exercise[6]
    return exercise

def loadExercises():
    validExerciseList = []
    with open("sets/list.csv", newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            exercise = formatAndFilterExercises(row)
            if exercise != None:
                validExerciseList.append(exercise)
    csvfile.close()
    return validExerciseList

def formatAndFilterExercises(exercise):
    if (exercise[0] != "Repetitions"): # Filter out the very first line (there probably is a better way to do this.
        # The first 3 should be ints.
        exercise[0] = int(exercise[0])
        exercise[1] = int(exercise[1])
        exercise[2] = int(exercise[2])

        # The last three should be booleans.
        exercise[6] = exercise[6] == "Y"
        exercise[7] = exercise[7] == "Y"
        exercise[8] = exercise[8] == "Y"
        if (settings["longDistance"] and exercise[1] > longDistanceLimit):
            return
        for styles in (exercise[3].split(" ")): # Filter out unwanted swimming styles.
            if not settings[styles]:
                return
        if (settings["longDistancePool"] and not exercise[8]):
            # Filter out impossible exercises because of long distance pools.
            return
        if (settings
            ["intensity"] < exercise[2]):
            return
        del exercise[8] #Delete the last boolean since it's no longer needed.
        return exercise

def saveSettings():
    settingsFile = open("config.swim", "wb")
    pickle.dump(settings, settingsFile)
    settingsFile.close()

def loadSettings():
    settingsFile = open("config.swim", "rb")
    global settings
    settings = pickle.load(settingsFile)
    settingsFile.close()

def getInput():
    settings["intensity"]= int(input("Intensity (1-100): "))
    settings["longDistance"] = bool(input("Allow long distances? (over 200m) (Y or N): ").upper() == "Y")
    settings["breaststroke"] = bool(input("Want to swim breaststroke? (Y or N): ").upper() == "Y")
    settings["backstroke"] = bool(input("Want to swim backstroke? (Y or N): ").upper() == "Y")
    settings["butterfly"] = bool(input("Want to swim butterfly? (Y or N): ").upper() == "Y")
    settings["medley"] = bool(input("Want to swim medley? (Y or N): ").upper() == "Y")
    settings["kick"] = bool(input("Want to do kicks? (Y or N): ").upper() == "Y")
    settings["longDistancePool"] = bool(input("Swimming in long distance pool? (Y (50m) or N (25m): ").upper() == "Y")
    settings["paddles"] = bool(input("Want to use paddles? (Y or N): ").upper() == "Y")
    settings["fins"] = bool(input("Want to use fins? (Y or N): ").upper() == "Y")
    settings["targetLength"] = int(input("About how many meters would you like to swim? "))

def checkDirOutput():
    if not os.path.isdir("outputPlans"):
        os.makedirs("outputPlans")

def main():
    checkDirOutput()
    loadSettingsBool = bool(input("Do you want to load settings(Y or N): ").upper() == "Y")
    if loadSettingsBool:
        loadSettings()
    else:
        getInput()
    validExerciseList = loadExercises()
    plan, length = makeExcercisePlan(validExerciseList)
    fileNamePlan = input("Please type in a file name for your newly generated plan: ")
    savePlanSpreadsheet(plan, length, fileNamePlan)
    if not loadSettingsBool:
        if bool(input("Do you want to save settings(Y or N): ").upper() == "Y"):
            saveSettings()

main()
