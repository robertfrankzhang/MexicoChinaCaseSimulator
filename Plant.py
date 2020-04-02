
class Plant:
    def __init__(self,sourcingCost,leadTime):
        self.sourcingCost = sourcingCost
        self.leadTime = leadTime

        #Parallel arrays
        self.unitsOnTheWay = []
        self.periodsUntilArrival = []

    def getUnitArriveIn(self,plusPeriod):
        total = 0
        for i in range(len(self.periodsUntilArrival)):
            if self.periodsUntilArrival[i] == 1:
                total += self.unitsOnTheWay[i]
        return total

    def getAllOnTheWay(self):
        total = 0
        for i in self.unitsOnTheWay:
            total += i
        return total