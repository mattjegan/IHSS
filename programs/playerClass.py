class Player():
    def __init__(self, playerID, firstName, lastName, number, games, goals, assists, shotsOn, misses, isGoalie, minors, majors, misconducts, matches, gameMisconducts):
        self.playerID = playerID
        self.firstName = firstName
        self.lastName = lastName
        self.number = number
        self.games = games
        self.goals = goals
        self.assists = assists
        self.isGoalie = isGoalie
        self.shotsOn = shotsOn
        self.misses = misses
        self.minors = minors
        self.majors = majors
        self.misconducts = misconducts
        self.matches = matches
        self.gameMisconducts = gameMisconducts

        self.recentMatch = 0
        self.recentGameMis = 0

        self.shotsOnThisGame = 0
        self.missesThisGame = 0
        self.goalsThisGame = 0
        self.assistsThisGame = 0

        self.points = self.goals + self.assists
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
    def addMinor(self):
        self.minors += 2
    def subMinor(self):
        self.minors -= 2
    def addMajor(self):
        self.majors += 5
    def subMajor(self):
        self.majors -= 5
    def addMisconduct(self):
        self.misconducts += 10
    def subMisconduct(self):
        self.misconducts -= 10
    def addMatch(self, left):
        self.matches += left
        self.recentMatch = left
    def subMatch(self):
        self.matches -= self.recentMatch
        self.recentMatch = 0
    def addGameMis(self, left):
        self.gameMisconducts += left + 48
        self.recentGameMis = left + 48
    def subGameMis(self):
        self.gameMisconducts -= self.recentGameMis
        self.recentGameMis = 0
    def getGoalieSavePercentage(self, inGame):
        if inGame == True:
            if self.shotsOnThisGame == 0:
                return "O shots"
            else:
                return 100*(1-(float(self.missesThisGame)/float(self.shotsOnThisGame)))
        else:
            if self.shotsOn == 0:
                return "0 shots"
            else:
                return 100*(1-(self.misses/self.shotsOn))
    def saveData(self, inGame):
        if inGame == True:
            return "-" + self.playerID + ";" + self.firstName + ";" + self.lastName + ";"  + str(self.number) + ";" + str(self.games) + ";" + str(self.goalsThisGame) + ";" + str(self.assistsThisGame) + ";" + str(self.shotsOnThisGame) + ";" + str(self.missesThisGame) + ";" + str(int(self.isGoalie)) + "\n Save Percentage: " + str(self.getGoalieSavePercentage(inGame))
        else:
            return "-" + self.playerID + ";" + self.firstName + ";" + self.lastName + ";"  + str(self.number) + ";" + str(self.games) + ";" + str(self.goals) + ";" + str(self.assists) + ";" + str(self.shotsOn) + ";" + str(self.misses) + ";" + str(int(self.isGoalie)) + ";" + str(self.minors) + ";" + str(self.majors) + ";" + str(self.misconducts) + ";" + str(self.matches) + ";" + str(self.gameMisconducts)