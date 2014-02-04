
def main():
    season = openSeason("hockeyData.txt")
    print season.teams[0].name
    season.teams[0].displayPlayers()

def openSeason(filename):
    # Transfer file into an array
    seasonFile = open(filename, "rU")
    seasonData = []
    for line in seasonFile:
        seasonData.append(line)

    # Create a season
    season = Season()
    teamPos = []
    nums = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    
    # Get team positions in array
    for e, item in enumerate(seasonData):
        if item[0] in nums:
            teamPos.append(e)

    # Get Team data
    for e, team in enumerate(teamPos):
        teamName = seasonData[team].split(".")[1].strip()
        newTeam = Team(teamName)
        try:
            currentTeam = seasonData[team+1:teamPos[e+1]]
        # Final team
        except:
            currentTeam = seasonData[team+1:]

        # Add players to team
        for player in currentTeam:
            playerData = player.split(";")
            newTeam.addPlayer(Player(playerData[0], playerData[1], playerData[2], playerData[3].strip()))
        
        # Add team to season
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
    # Add a player object to the players array
    def addPlayer(self, player):
        self.players.append(player)
    # Display some stats from players in the team
    def displayPlayers(self):
        for player in self.players:
            print player.name, player.goals, player.assists
    # Record a goal
    def goalScored(self, playerNum, assistNum=""):
        for player in self.players:
            if player.number == playerNum:
                player.addGoal()
            if player.number == assistNum:
                player.addAssist()
    # Record a win
    def addWin(self):
        self.wins += 1
    # Record a loss
    def addLoss(self):
        self.loses += 1

class Player():
    def __init__(self, name, number, goals=0, assists=0):
        self.name = name
        self.number = number
        self.goals = goals
        self.assists = assists
    # Add a goal
    def addGoal(self):
        self.goals += 1
    # Add an assist
    def addAssist(self):
        self.assists += 1

if __name__ == "__main__": main()
