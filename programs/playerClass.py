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
            self.shotsOn = goals
            self.misses = assists

            self.shotsOnThisGame = 0
            self.missesThisGame = 0

        self.goalsThisGame = 0
        self.assistsThisGame = 0
    def getFullName(self):
        if self.isGoalie == True:
            return str(self.number) + " [G] " + self.firstName + " " + self.lastName
        else:
            return str(self.number) + " " + self.firstName + " " + self.lastName
    def addGoal(self):
        self.goals += 1
        self.goalsThisGame += 1
    def subGoal(self):
        self.goals -= 1
        self.goalsThisGame -= 1
    def addAssist(self):
        self.assists += 1
        self.assistsThisGame += 1
    def subAssist(self):
        self.assists -= 1
        self.assistsThisGame -= 1
    def addShotsOn(self):
        self.shotsOn += 1
        self.shotsOnThisGame += 1
    def subShotsOn(self):
        self.shotsOn -= 1
        self.shotsOnThisGame -= 1
    def addMiss(self):
        self.misses += 1
        self.missesThisGame += 1
    def subMiss(self):
        self.misses -= 1
        self.missesThisGame -= 1
    def getGoalieSavePercentage(self):
        return 100*(1-(self.misses/self.shotsOn))
    def saveData(self, inGame):
        if inGame == True:
            if self.isGoalie == False:
                return "-" + self.firstName + ";" + self.lastName + ";"  + str(self.number) + ";" + str(self.games) + ";" + str(self.goalsThisGame) + ";" + str(self.assistsThisGame) + ";" + str(0)
            elif self.isGoalie == True:
                return "-" + self.firstName + ";" + self.lastName + ";"  + str(self.number) + ";" + str(self.games) + ";" + str(self.shotsOnThisGame) + ";" + str(self.missesThisGame) + ";" + str(1)
        else:
            if self.isGoalie == False:
                return "-" + self.firstName + ";" + self.lastName + ";"  + str(self.number) + ";" + str(self.games) + ";" + str(self.goals) + ";" + str(self.assists) + ";" + str(0)
            elif self.isGoalie == True:
                return "-" + self.firstName + ";" + self.lastName + ";"  + str(self.number) + ";" + str(self.games) + ";" + str(self.shotsOn) + ";" + str(self.misses) + ";" + str(1)