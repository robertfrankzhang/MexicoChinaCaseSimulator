
from Firm import Firm
from HistorialDataGenerator import HistoricalDataGenerator
from scipy.stats import norm
import csv
import numpy as np
import math

dataGenerator = HistoricalDataGenerator()

numPeriods = dataGenerator.numPeriods
SKUCount = dataGenerator.numSKU

###Control Panel####
modesToTry = [10]
#SKUsToTry = [0,1,2,3,4,5,6,7,8,9]
SKUsToTry = [0,1,2,3,4,5,6,7,8,9]
####################

with open("modeEval.csv", mode='w') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    m = []
    for i in modesToTry:
        m.append(i)
    writer.writerow(m)

    cashes = []
    invs = []
    for mode in modesToTry:
        allCashHistory = []
        allInvHistory = []
        for SKU in SKUsToTry:
            dataGenerator.reset(SKU=SKU)
            firm = Firm()
            firm.addPlant("China", 7250, 4)
            firm.addPlant("Mexico", 8000, 1)
            cashHistory = []
            invHistory = []
            for i in range(numPeriods):
                demand = dataGenerator.getNext()
                firm.runPeriod(demand)

                # Make sourcing decisions############################################################################################
                if mode == 0:
                    if i < numPeriods:
                        SLChina = 0.9
                        mean, sd = dataGenerator.getMeanSDOfPeriod(i)
                        amount = max(0, norm.ppf(SLChina) * sd + mean- firm.unitInventoryOnHand/5)  # NORM.INV based on SL
                        # print(amount)
                        firm.sourceUnit("China", amount)

                elif mode == 1: #Maximal amount = rop-onhand Mexico SL (approx 3.9M)
                    if i < numPeriods-2:
                        SLMexico = 0.9
                        mean1, sd1 = dataGenerator.getMeanSDOfPeriod(i + 1)

                        safetyStock = norm.ppf(SLMexico) * sd1
                        ROP = safetyStock + mean1
                        if firm.unitInventoryOnHand < ROP:
                            amount = ROP-firm.unitInventoryOnHand
                        else:
                            amount = 0
                        print(amount)
                        firm.sourceUnit("Mexico", amount)

                elif mode == 2: #Maximal amount = mean4 China SL (approx 4.7M)
                    if i < numPeriods-5:
                        SLChina = 0.1
                        mean1, sd1 = dataGenerator.getMeanSDOfPeriod(i + 1)
                        mean2, sd2 = dataGenerator.getMeanSDOfPeriod(i + 2)
                        mean3, sd3 = dataGenerator.getMeanSDOfPeriod(i + 3)
                        mean4, sd4 = dataGenerator.getMeanSDOfPeriod(i + 4)

                        safetyStock = norm.ppf(SLChina) * math.sqrt(math.pow(sd1,2)+math.pow(sd2,2)+math.pow(sd3,2)+math.pow(sd4,2))
                        print("SAFETY: "+str(safetyStock))
                        ROP = safetyStock + mean1+mean2+mean3+mean4
                        print("ROP: "+str(ROP))
                        print('MEAN4: '+str(mean4))
                        if firm.unitInventoryOnHand < ROP:
                            amount = norm.ppf(SLChina) * sd4 + mean4  # NORM.INV based on SL
                            amount = mean4
                        else:
                            amount = 0
                        print(amount)
                        print()
                        firm.sourceUnit("China", amount)

                elif mode == 2.1:
                    if i < numPeriods-5:
                        SLChina = 0.7
                        mean1, sd1 = dataGenerator.getMeanSDOfPeriod(i + 1)
                        mean2, sd2 = dataGenerator.getMeanSDOfPeriod(i + 2)
                        mean3, sd3 = dataGenerator.getMeanSDOfPeriod(i + 3)
                        mean4, sd4 = dataGenerator.getMeanSDOfPeriod(i + 4)

                        safetyStock = norm.ppf(SLChina) * math.sqrt(math.pow(sd1,2)+math.pow(sd2,2)+math.pow(sd3,2)+math.pow(sd4,2))
                        ROP = safetyStock + mean1+mean2+mean3+mean4
                        if firm.unitInventoryOnHand < ROP:
                            amount = norm.ppf(SLChina) * sd4 + mean4  # NORM.INV based on SL
                            amount = mean4
                        else:
                            amount = 0
                        print(amount)
                        firm.sourceUnit("China", amount)

                elif mode == 2.2: #Maximal amount = mean4 China SL (approx 4.7M)
                    if i < numPeriods-5:
                        SLChina = 0.9
                        mean1, sd1 = dataGenerator.getMeanSDOfPeriod(i + 1)
                        mean2, sd2 = dataGenerator.getMeanSDOfPeriod(i + 2)
                        mean3, sd3 = dataGenerator.getMeanSDOfPeriod(i + 3)
                        mean4, sd4 = dataGenerator.getMeanSDOfPeriod(i + 4)

                        safetyStock = norm.ppf(SLChina) * math.sqrt(math.pow(sd1,2)+math.pow(sd2,2)+math.pow(sd3,2)+math.pow(sd4,2))
                        ROP = safetyStock + mean1+mean2+mean3+mean4

                        if firm.unitInventoryOnHand < ROP:
                            amount = norm.ppf(SLChina) * sd4 + mean4  # NORM.INV based on SL
                            amount = mean1 + mean2 + mean3 + mean4
                        else:
                            amount = 0
                        print(amount)
                        firm.sourceUnit("China", amount)

                elif mode == 3: #3.69M
                    if i < numPeriods - 2:
                        SLMexico = 0.992
                        mean1, sd1 = dataGenerator.getMeanSDOfPeriod(i + 1)

                        safetyStock = norm.ppf(SLMexico) * sd1
                        if firm.unitInventoryOnHand < safetyStock:
                            amount = safetyStock-firm.unitInventoryOnHand+mean1
                        else:
                            amount = 0
                        print(amount)
                        firm.sourceUnit("Mexico", amount)

                elif mode == 4: #2.83M
                    if i < numPeriods-5:
                        SLChina = 0.992
                        mean1, sd1 = dataGenerator.getMeanSDOfPeriod(i + 1)
                        mean2, sd2 = dataGenerator.getMeanSDOfPeriod(i + 2)
                        mean3, sd3 = dataGenerator.getMeanSDOfPeriod(i + 3)
                        mean4, sd4 = dataGenerator.getMeanSDOfPeriod(i + 4)
                        safetyStock = norm.ppf(SLChina) * math.sqrt(math.pow(sd1,2)+math.pow(sd2,2)+math.pow(sd3,2)+math.pow(sd4,2))

                        amount = max(0, safetyStock - firm.unitInventoryOnHand + mean4)

                        print(amount)
                        firm.sourceUnit("China", amount)

                elif mode == 5: #4.15M
                    if i < numPeriods-5:
                        mean4, sd4 = dataGenerator.getMeanSDOfPeriod(i + 4)
                        amount = mean4
                        print(amount)
                        firm.sourceUnit("China", amount)

                elif mode == 5.1:
                    if i < numPeriods-5:
                        mean1, sd1 = dataGenerator.getMeanSDOfPeriod(i + 1)
                        mean2, sd2 = dataGenerator.getMeanSDOfPeriod(i + 2)
                        mean3, sd3 = dataGenerator.getMeanSDOfPeriod(i + 3)
                        mean4, sd4 = dataGenerator.getMeanSDOfPeriod(i + 4)
                        SLChina = 2750 / (2750 + 7250 * (math.pow(1.01, numPeriods - i - 1) - 1))
                        safetyStock = norm.ppf(SLChina) * math.sqrt(math.pow(sd1, 2) + math.pow(sd2, 2) + math.pow(sd3, 2) + math.pow(sd4, 2))
                        ROP = safetyStock + mean1 + mean2 + mean3 + mean4

                        amount = max(0,firm.unitInventoryOnHand - mean4)
                        print(amount)
                        firm.sourceUnit("China", amount)

                elif mode == 6: #3.01M
                    if i < numPeriods-2:
                        mean1, sd1 = dataGenerator.getMeanSDOfPeriod(i + 1)
                        amount = mean1
                        print(amount)
                        firm.sourceUnit("Mexico", amount)

                elif mode == 7: #4.26M (Maximal SL)
                    if i < numPeriods - 5:
                        SLChina = 0.7
                        mean4, sd4 = dataGenerator.getMeanSDOfPeriod(i + 4)
                        safetyStock = norm.ppf(SLChina) * sd4
                        amount = max(0,safetyStock - firm.unitInventoryOnHand + mean4)
                        print(amount)
                        firm.sourceUnit("China", amount)

                elif mode == 8: #4.29M******
                    if i < numPeriods - 5:
                        SLChina = 2750/(2750+7250*(math.pow(1.01,numPeriods-i-1)-1))
                        mean4, sd4 = dataGenerator.getMeanSDOfPeriod(i + 4)
                        safetyStock = norm.ppf(SLChina) * sd4

                        amount = max(0,safetyStock + mean4 - firm.unitInventoryOnHand)
                        #print(amount)
                        firm.sourceUnit("China", amount)

                elif mode == 8.1: #4.29M******
                    if i < numPeriods - 5:
                        SLChina = 0.9
                        mean4, sd4 = dataGenerator.getMeanSDOfPeriod(i + 4)
                        safetyStock = norm.ppf(SLChina) * sd4

                        amount = max(0,safetyStock + mean4 - firm.unitInventoryOnHand)
                        print(amount)
                        firm.sourceUnit("China", amount)

                elif mode == 9: #3.62M
                    if i < numPeriods - 2:
                        SLChina = 2750/(2750+7250*(math.pow(1.01,numPeriods-i-1)-1))
                        mean1, sd1 = dataGenerator.getMeanSDOfPeriod(i + 1)
                        safetyStock = norm.ppf(SLChina) * sd1

                        amount = max(0,safetyStock - firm.unitInventoryOnHand + mean1)
                        print(amount)
                        firm.sourceUnit("Mexico", amount)

                elif mode == 10:
                    SL = (10000-7250)/(2750+7250*(math.pow(1.01,4)-1))
                    mexOrder = 0
                    chinaOrder = 0
                    if i < numPeriods - 2:
                        mean1, sd1 = dataGenerator.getMeanSDOfPeriod(i + 1)
                        mexOrder = max(0, norm.ppf(SL) * sd1 + mean1 - firm.unitInventoryOnHand - firm.plants['China'].getUnitArriveIn(1))
                        firm.sourceUnit("Mexico", mexOrder)
                    if i < numPeriods - 5:
                        mean2, sd2 = dataGenerator.getMeanSDOfPeriod(i + 2)
                        mean3, sd3 = dataGenerator.getMeanSDOfPeriod(i + 3)
                        mean4, sd4 = dataGenerator.getMeanSDOfPeriod(i + 4)
                        expInvIn4 = firm.unitInventoryOnHand - mean1 - mean2 - mean3 + firm.plants["China"].getAllOnTheWay() + mexOrder
                        chinaOrder = max(0,norm.ppf(SL,mean4,sd4)-expInvIn4)
                        firm.sourceUnit("China",chinaOrder)
                        #print(chinaOrder)
                    print(chinaOrder)

                ####################################################################################################################

                # Print Cash
                cashHistory.append(firm.cash)
                if demand == 0 and firm.unitInventoryOnHand+demand == 0:
                    invHistory.append(math.log10(1))
                elif demand == 0:
                    invHistory.append(math.log10(firm.unitInventoryOnHand+demand))
                elif firm.unitInventoryOnHand == 0:
                    invHistory.append(math.log10(1/demand))
                else:
                    invHistory.append(math.log10((firm.unitInventoryOnHand+demand)/demand))
            allCashHistory.append(cashHistory)
            allInvHistory.append(invHistory)
        npCH = np.transpose(np.array(allCashHistory))
        npIH = np.transpose(np.array(allInvHistory))
        avgCH = []
        for p in npCH:
            avgCH.append(np.mean(p))
        cashes.append(avgCH)

        avgIH = []
        for p in npIH:
            avgIH.append(np.mean(p))
        invs.append(avgIH)
    cashExp = np.transpose(np.array(cashes))
    for i in cashExp:
        writer.writerow(i.tolist())

    writer.writerow([])
    writer.writerow(m)
    invExp = np.transpose(np.array(invs))
    for i in invExp:
        writer.writerow(i.tolist())

