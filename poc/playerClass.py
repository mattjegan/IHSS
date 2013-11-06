class Player():
    def __init__(self, firstName, lastName, number, games, goals, assists, isGoalie=False):
        self.firstName = firstName
        self.lastName = lastName
        self.number = number
        self.games = games
        self.goals = goals
        self.assists = assists
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
    def addShotsOn(self):
        self.shotsOn += 1
    def subShotsOn(self):
        self.shotsOn -= 1
    def getGoalieSavePercentage(self):
        return 100*(1-(self.misses/self.shotsOn))
    def saveData(self):
        return "-" + self.firstName + ";" + self.lastName + ";"  + str(self.number) + ";" + str(self.games) + ";" + str(self.goals) + ";" + str(self.assists) + ";" + str(int(self.isGoalie))