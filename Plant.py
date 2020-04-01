
class Plant:
    def __init__(self,sourcingCost,leadTime):
        self.sourcingCost = sourcingCost
        self.leadTime = leadTime

        #Parallel arrays
        self.unitsOnTheWay = []
        self.periodsUntilArrival = []