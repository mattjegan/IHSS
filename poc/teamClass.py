import math

class Team():
    def __init__(self, teamName):
        self.teamName = teamName
        self.players = []
        self.totalGoals = 0
        self.totalGoalsAgainst = 0
    def addPlayer(self, player):
        self.players.append(player)
    def removePlayer(self, playerNumber):
        for e, player in enumerate(self.players):
            if player.number == playerNumber:
                self.players.remove(e)
    def addGoal(self): #goalPlayerNumber, assistPlayerNumber=math.pi, assist2PlayerNumber=math.pi):
        self.totalGoals += 1
        #for player in self.players:
        #    if player.number == goalPlayerNumber:
        #        player.addGoal()
        #    elif player.number == assistPlayerNumber:
        #        player.addAssist()
        #    elif player.number == assist2PlayerNumber:
        #        player.addAssist()
    def goalAgainst(self):
        self.totalGoalsAgainst += 1