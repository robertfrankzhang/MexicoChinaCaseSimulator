
from Firm import Firm
from scipy.stats import norm
from HistorialDataGenerator import HistoricalDataGenerator
import numpy as np
import math

dataGenerator = HistoricalDataGenerator()

numPeriods = dataGenerator.numPeriods
SKUCount = dataGenerator.numSKU

firm = Firm()
firm.addPlant("China", 7250, 4)
firm.addPlant("Mexico", 8000, 1)

periodCount = 0
while True:
    print("Period "+str(periodCount+1))
    while True:
        try:
            demand = int(input("Please enter the demand\n"))
            break
        except ValueError:
            print("Demand must be int try again")

    while True:
        answer = input("Are you sure demand is "+str(demand)+"?")
        if answer == "yes":
            break

    firm.runPeriod(demand)
    SL = (10000 - 7250) / (2750 + 7250 * (math.pow(1.01, 4) - 1))
    mexOrder = 0
    chinaOrder = 0
    if periodCount < numPeriods - 2:
        mean1, sd1 = dataGenerator.getMeanSDOfPeriod(periodCount + 1)
        mexOrder = max(0,norm.ppf(SL) * sd1 + mean1 - firm.unitInventoryOnHand - firm.plants['China'].getUnitArriveIn(1))
        firm.sourceUnit("Mexico", mexOrder)
    if periodCount < numPeriods - 5:
        mean2, sd2 = dataGenerator.getMeanSDOfPeriod(periodCount + 2)
        mean3, sd3 = dataGenerator.getMeanSDOfPeriod(periodCount + 3)
        mean4, sd4 = dataGenerator.getMeanSDOfPeriod(periodCount + 4)
        expInvIn4 = firm.unitInventoryOnHand - mean1 - mean2 - mean3 + firm.plants["China"].getAllOnTheWay() + mexOrder
        chinaOrder = max(0, norm.ppf(SL, mean4, sd4) - expInvIn4)
        firm.sourceUnit("China", chinaOrder)
    print("Period "+str(periodCount)+" China Order: "+str(chinaOrder))
    print("Period "+str(periodCount)+" Mexico Order: "+str(mexOrder))
    periodCount += 1
    print("##############################################################")
    print()