
def main():
    #assassins = Team("Assassins")
    #print assassins.name

    #assassins.addPlayer(Player("Matt", 80, 5))
    #assassins.addPlayer(Player("Tim", 13, 9))

    #assassins.displayPlayers()
    #print ""

    #assassins.goalScored(80, 13)
    #assassins.displayPlayers()
    season = openSeason("hockeyData.txt")
    season.teams[0].displayPlayers()

def openSeason(filename):
    seasonFile = open(filename, "rU")
    seasonData = []
    for line in seasonFile:
        seasonData.append(line)

    season = Season()
    teamPos = []
    nums = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    
    # Get team positions in array
    for e, item in enumerate(seasonData):
        if item[0] in nums:
            teamPos.append(e)

    # Get Team data
    for e, team in enumerate(teamPos):
        newTeam = Team(seasonData[team])
        try:
            currentTeam = seasonData[team+1:teamPos[e+1]]
        # Final team
        except:
            currentTeam = seasonData[team+1:]

        for player in currentTeam:
            playerData = player.split(";")
            newTeam.addPlayer(Player(playerData[0], playerData[1], playerData[2], playerData[3].strip()))
        
        season.addTeam(newTeam)
        
    return season


class Season():
    def __init__(self):
        self.teams = []
    def addTeam(self, team):
        self.teams.append(team)

class Team():
    def __init__(self, name):
        self.name = name
        self.players = []
        self.wins = 0
        self.loses = 0
    def addPlayer(self, player):
        self.players.append(player)
    def displayPlayers(self):
        for player in self.players:
            print player.name, player.goals, player.assists
    def goalScored(self, playerNum, assistNum=""):
        for player in self.players:
            if player.number == playerNum:
                player.addGoal()
            if player.number == assistNum:
                player.addAssist()
    def addWin(self):
        self.wins += 1
    def addLoss(self):
        self.loses += 1

class Player():
    def __init__(self, name, number, goals=0, assists=0):
        self.name = name
        self.number = number
        self.goals = goals
        self.assists = assists
    def addGoal(self):
        self.goals += 1
    def addAssist(self):
        self.assists += 1

if __name__ == "__main__": main()
