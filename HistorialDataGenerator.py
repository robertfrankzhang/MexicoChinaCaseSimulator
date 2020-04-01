
import pandas as pd
import random
import csv
import numpy as np

class HistoricalDataGenerator:
    def __init__(self,inputFile="SampleData.csv",statsFileName="meanAndSD.csv",SKU=None):
        data = pd.read_csv(inputFile,sep=",")
        self.dataFeatures = data.values
        self.numSKU = self.dataFeatures[0].size
        self.numPeriods = self.dataFeatures.shape[0]
        if SKU == None:
            self.currentSKU = random.randint(0,self.numSKU)     #Current historical SKU testing
        else:
            self.currentSKU = SKU
        self.current = self.dataFeatures[:,self.currentSKU] #Current historical data array
        self.currentIndex = 0

        with open(statsFileName,mode='w') as file:
            writer = csv.writer(file,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["Mean","Std Deviation"])
            for period in self.dataFeatures:
                writer.writerow([np.mean(period),np.std(period)])
        self.statsFileName = statsFileName
        self.periodStats = pd.read_csv(self.statsFileName, sep=",").values

    def reset(self,SKU=None):
        if SKU == None:
            self.currentSKU = random.randint(0, self.numSKU)  # Current historical SKU testing
        else:
            self.currentSKU = SKU
        self.current = self.dataFeatures[:, self.currentSKU]  # Current historical data array
        self.currentIndex = 0

    def getNext(self):
        next = self.current[self.currentIndex]
        self.currentIndex += 1
        # if self.currentIndex == self.numPeriods:
        #     print("No more periods")
        return next

    def getMeanSDOfPeriod(self,period): #Periods start at 0, so 0 is first demand
        return (self.periodStats[period,0],self.periodStats[period,1])



