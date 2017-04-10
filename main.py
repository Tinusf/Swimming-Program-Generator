import csv
import random

settings = {}

# Default settings, you can change these if you want to.
chanceForFins = 50 #% chance
chanceForPaddles = 50 #% chance

warmUpExercise = [1, 400, 20, "freestyle", "Warm up", "05:00", False, False]
warmDownExercise = [1, 200, 20, "freestyle", "Warm down", "05:00", False, False]

deltaLength = 500 # Maybe rename this variable to something else?
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
    settings["targetLength"] = 3500

def savePlanTxt():
    # Don't really need this tbh.
    pass

def savePlanSpreadsheet(plan, length, fileName):
    with open("outputPlans/" + fileName + ".csv", "w", newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Reps', 'Dist', 'Intensity', 'Style(s)', 'Description', 'Start time / Pause', 'Fins', 'Paddles'])
        for exercise in plan:
            print(exercise)
            spamwriter.writerow(exercise)
        spamwriter.writerow(['', '', '', '', 'Total exercise length: ' + str(length)])
    print("Saved your plan at outputPlans/" + fileName + ".csv")
    csvfile.close()

def printPlan(plan):
    pass

def makeExcercisePlan(validPlans):
    currentPlan = []
    totalLength = 0
    totalDelta = deltaLength + (warmDownExercise[1] * warmDownExercise[0])
    # This is the length of the warm down plus the deltaLength.
    print(totalDelta)
    currentPlan.append(warmUpExercise)
    totalLength += warmUpExercise[0] * warmUpExercise[1]
    while totalLength < settings["targetLength"] + totalDelta:
        curRNG = random.randint(0, len(validPlans) -1)
        curExercise = validPlans[curRNG]
        curLength = (curExercise[0] * curExercise[1])
        if (totalLength + curLength) < settings["targetLength"] + totalDelta:
            if (settings["paddles"] and curExercise[7]):
                curExercise[7] = chanceForPaddles >= random.randint(1, 100)
            else:
                curExercise[7] = False

            if (settings["fins"] and curExercise[6]):
                curExercise[6] = chanceForFins >= random.randint(1, 100)
            else:
                curExercise[6] = False

            currentPlan.append(curExercise)
            totalLength += curLength
            # del validPlans[curRNG] #Do this when you have enough different exercises.
        else:
            # TODO, Try again with a shorter exercise.
            # Maybe just delete it from the list and try again, but after a while it should stop trying.
            break
    totalLength += warmDownExercise[0] * warmDownExercise[1]
    currentPlan.append(warmDownExercise)
    return currentPlan, totalLength


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

def formatAndFilterExercises(excercise):
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
        del excercise[8] #Delete the last boolean since it's no longer needed.
        return excercise


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
    settings["targetLength"] = int(input("About how many meters would you like to swim?"))

def main():
    #getInput()
    testingSettings()
    validExerciseList = loadExercises()
    print(validExerciseList)
    plan, length = makeExcercisePlan(validExerciseList)
    fileName = input("Please type in a file name for your newly generated plan: ")
    savePlanSpreadsheet(plan, length, fileName)
    printPlan(plan)

main()