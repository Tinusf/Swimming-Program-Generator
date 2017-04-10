import csv
import random

settings = {}

# Default settings, you can change these if you want to.
chanceForFins = 50 #% chance
chanceForPaddles = 50 #% chance

warmUpExercise = [1, 400, 0, "freestyle", "Warm up", "05:00"]
warmDownExercise = [1, 200, 0, "freestyle", "Warm down", "05:00"]

deltaLength = 500 # Maybe rename this variable to something else?
settings["crawl"] = True
settings["special"] = True
settings["freestyle"] = True


def testingSettings():
    # Run this function when you are testing instead of running getInput()
    settings["intensity"] = 50
    settings["longDistance"] = True
    settings["breastroke"] = True
    settings["backstroke"] = False
    settings["butterfly"] = False
    settings["medley"] = False
    settings["kick"] = True
    settings["longDistancePool"] = False
    settings["paddles"] = True
    settings["fins"] = True
    settings["targetLength"] = 3500

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

    totalDelta = deltaLength + (warmDownExercise[1] * warmDownExercise[0])
    # This is the length of the warm down plus the deltaLength.
    currentPlan.append(warmUpExercise)
    totalLength += warmUpExercise[0] * warmUpExercise[1]
    while totalLength < settings["targetLength"] + totalDelta:
        curRNG = random.randint(0, len(validPlans) -1)
        curExercise = validPlans[curRNG]
        curLength = (curExercise[0] * curExercise[1])
        if (totalLength + curLength) < settings["targetLength"] + totalDelta:
            curExerciseFormat = formatDescription(curExercise)
            currentPlan.append(curExerciseFormat)
            totalLength += curLength
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
        if (settings["longDistance"] and exercise[1] > 200):
            return
        for styles in (exercise[3].split(" ")): # Filter out unwanted swimming styles.
            if not settings[styles]:
                return
        if (settings["longDistancePool"] and not exercise[8]):
            # Filter out impossible exercises because of long distance pools.
            return
        del exercise[8] #Delete the last boolean since it's no longer needed.
        return exercise

def saveSettings():
    pass

def loadSettings():
    pass

def getInput():
    settings["intensity"]= int(input("Intensity (1-100): "))
    settings["longDistance"] = bool(input("Allow long distances? (over 200m)(Y or N): ").upper() == "Y")
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
    getInput()
    validExerciseList = loadExercises()
    plan, length = makeExcercisePlan(validExerciseList)
    fileName = input("Please type in a file name for your newly generated plan: ")
    savePlanSpreadsheet(plan, length, fileName)

main()
