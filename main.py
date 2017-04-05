def savePlanTxt():
    pass

def savePlanSpreadsheet():
    pass

def printPlan():
    pass

def makeExcercisePlan():
    pass

def loadExercises():
    pass

def getInput():
    intensity = int(input("Intensity (1-100): "))
    breastroke = bool(input("Want to swim breaststroke?(Y or N): ").upper() == "Y")
    backstroke = bool(input("Want to swim backstroke?(Y or N): ").upper() == "Y")
    butterfly = bool(input("Want to swim butterfly?(Y or N): ").upper() == "Y")
    longDistancePool = bool(input("Swimming in long distance pool?(Y (50m) or N (25m): ").upper() == "Y")
    equipment = bool(input("Want to use equipment?(Y or N): ").upper() == "Y")
    if (equipment):
        pass

    return intensity, breastroke

def main():
    args = getInput()
    print(args)





main()