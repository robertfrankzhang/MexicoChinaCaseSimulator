from Plant import Plant
import copy

class Firm:
    def __init__(self,salePrice = 10000,cashReturnPP = 0.01,debtCostPP = 0.01):
        self.salePrice = salePrice
        self.cashReturn = cashReturnPP
        self.debtCost = debtCostPP
        self.cash = 0
        self.unitInventoryOnHand = 0
        self.plants = {}

    def runPeriod(self,periodDemand): #Run this period, and THEN make sourcing decisions
        #Appreciate/depreciate cash
        if self.cash > 0:
            self.cash *= 1+self.cashReturn
        if self.cash < 0:
            self.cash *= 1+self.debtCost

        #Decrement periodsUntilArrival
        for plantID,plant in self.plants.items():
            for i in range(len(plant.periodsUntilArrival)):
                plant.periodsUntilArrival[i] -= 1
            self.plants[plantID] = plant

        #Update inventory on hand based on arriving orders w/ periods = 0
        for plantID,plant in self.plants.items():
            newUntilArrival = []
            newOnWay = []
            for i in range(len(plant.periodsUntilArrival)):
                if plant.periodsUntilArrival[i] == 0:
                    self.unitInventoryOnHand += plant.unitsOnTheWay[i]
                else:
                    newUntilArrival.append(plant.periodsUntilArrival[i])
                    newOnWay.append(plant.unitsOnTheWay[i])
            plant.unitsOnTheWay = newOnWay
            plant.periodsUntilArrival = newUntilArrival
            self.plants[plantID] = plant

        #Make sales based on demand
        sold = min(self.unitInventoryOnHand,periodDemand)
        self.cash += sold*self.salePrice
        self.unitInventoryOnHand -= sold

        #Make Sourcing Decisions By Purchasing New Inventory (Not in this method but in main)

        #Print Cash for this period (Not in this method but in main)

    def addPlant(self,ID,sourcingCost,leadTime):
        self.plants[ID] = Plant(sourcingCost,leadTime)

    def sourceUnit(self,plantID,amount):
        plant = self.plants[plantID]
        self.cash -= plant.sourcingCost*amount
        plant.unitsOnTheWay.append(amount)
        plant.periodsUntilArrival.append(plant.leadTime)
        self.plants[plantID] = plant