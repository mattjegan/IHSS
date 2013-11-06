class Player():
    def __init__(self, firstName, lastName, number, isGoalie=False):
        self.firstName = firstName
        self.lastName = lastName
        self.number = number
        self.games = 0
        self.goals = 0
        self.assists = 0
        self.isGoalie = isGoalie
        if self.isGoalie == True:
            self.shotsOn = 0
            self.misses = 0
    def addGoal(self):
        self.goals += 1
    def subGoal(self):
        self.goals -= 1
    def addAssist(self):
        self.assists += 1
    def subAssist(self):
        self.assists -= 1
    def getGoalieSavePercentage(self):
        return 100*(1-(self.misses/self.shotsOn))