from Tkinter import *
import ttk

import datetime

import teamClass
import playerClass

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.teamList = []
        self.pack()
        self.maxTeamPlayers = 2
        self.loadData()
        self.gameNumber = int([line for line in open("gameNumber.txt", "rU")][0])
        self.teamNames = []
        for team in self.teamList:
            self.teamNames.append(team.teamName)
        self.team1 = self.teamList[0]
        self.team2 = self.teamList[1]
        self.team1score = 0
        self.team2score = 0
        self.actions = []

        nullPlayer = playerClass.Player(0, "0", "0", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

        for player in self.team1.players:
            if player.isGoalie:
                self.team1currentGoalie = player
                break
            else:
                self.team1currentGoalie = nullPlayer

        for player in self.team2.players:
            if player.isGoalie:
                self.team2currentGoalie = player
                break
            else:
                self.team2currentGoalie = nullPlayer

        self.createWidgets()

    def addTeam(self, team):
        self.teamList.append(team)

    def loadData(self):
        dataFile = open("teamData.txt", "rU")
        dataArray = [line for line in dataFile]
        dataFile.close()

        teams = []
        currentTeam = -1
        players = 0

        for item in dataArray:
            if str(item)[0] != '-':
                currentTeam += 1
                newTeam = teamClass.Team(str(item).strip())
                teams.append(newTeam)

                if players > self.maxTeamPlayers:
                    self.maxTeamPlayers = players

                players = 0
            else:
                players += 1
                # (self, playerID, firstName, lastName, number, isGoalie=False)
                playerData = [part for part in item.strip().split(';')]

                # Remove minus sign
                playerData[0] = playerData[0][1:]

                # Set isGoalie flag
                if int(playerData[9]) == 0:
                    playerData[9] = False
                else:
                    playerData[9] = True

                newPlayer = playerClass.Player(playerData[0], playerData[1], playerData[2], int(playerData[3]), int(playerData[4]), int(playerData[5]), int(playerData[6]), int(playerData[7]), int(playerData[8]), int(playerData[9]), int(playerData[10]), int(playerData[11]), int(playerData[12]), int(playerData[13]), int(playerData[14]))
                # Assign to team
                teams[currentTeam].addPlayer(newPlayer)

        for team in teams:
            self.addTeam(team)

    def saveData(self):
        ## Save individual game stats
        gameFileName = "savedGames/game" + str(self.gameNumber) + ".txt"
        gameFile = open(gameFileName, "w")
        gameFile.write(str(self.gameNumber))
        gameFile.write("\n")
        gameFile.write(self.dateVar.get())
        gameFile.write("\n")
        gameFile.write(self.timeVar.get())
        gameFile.write("\n")
        gameFile.write(self.ref1Var.get())
        gameFile.write("\n")
        gameFile.write(self.ref2Var.get())
        gameFile.write("\n")
        gameFile.write(self.scorerVar.get())
        gameFile.write("\n")
        gameFile.write(self.timekeeperVar.get())
        gameFile.write("\n")
        gameFile.write("\n")
        gameFile.write(str(self.team1score)+"v"+str(self.team2score))
        gameFile.write("\n")
        gameFile.write("\n")

        ## Team 1 information
        gameFile.write(self.team1.teamName)
        for player in self.team1.players:
            gameFile.write("\n")
            gameFile.write(player.saveData(True))

        gameFile.write("\n")

        ## Team 2 Information
        gameFile.write(self.team2.teamName)
        for player in self.team2.players:
            gameFile.write("\n")
            gameFile.write(player.saveData(True))

        gameFile.write("\n\n")

        ## Action summary
        for e, item in enumerate(self.actions):
            if item == "-":
                del self.actions[e]
                del self.actions[e-1]
        for item in self.actions:
            gameFile.write(item + "\n")

        gameFile.close()

        ## Update game number for next game
        self.gameNumber += 1
        gameNFile = open("gameNumber.txt", "w")
        gameNFile.write(str(self.gameNumber))
        gameNFile.close()

        ## Save overall player stats
        teamData = []
        for team in self.teamList:
            teamData.append(team.teamName)
            for player in team.players:
                teamData.append(player.saveData(False))

        self.quit()
        dataFile = open("teamData.txt", "w")
        for item in teamData:
            dataFile.write(item + "\n")
        dataFile.close()

        self.saveHTMLTable()

    def saveHTMLTable(self):
        htmlFileName = "htmlTables/table" + str(self.gameNumber) + ".html"
        htmlFile = open(htmlFileName, "w")
        
        ## Write html constants for table including headers
        htmlFile.write("""<table border="1">""")
        htmlFile.write("""<tr>
<th>Name</th>
<th>#</th>
<th>G</th>
<th>A</th>
<th>P</th>
</tr>""")

        ## Write each players stats
        for team in self.teamList:
            for player in team.players:
                stringToWrite = "<tr><td>" + player.getFullName() + "</td><td>" + str(player.number) + "</td><td>" + str(player.goals) + "</td><td>" + str(player.assists) + "</td><td>" + str(player.goals + player.assists) + "</td></tr>"
                htmlFile.write(stringToWrite)

        htmlFile.close()

    def saveAllTimeData(self):
        ## Save overall player stats
        teamData = []
        for team in self.teamList:
            teamData.append(team.teamName)
            for player in team.players:
                teamData.append(player.saveData(False))

        dataFile = open("teamData.txt", "w")
        for item in teamData:
            dataFile.write(item + "\n")
        dataFile.close()

    def createWidgets(self):
        WIDTH = 10
        ## Date, time and officals area
        admin = Frame(self)
        admin.grid(row=0, column=0)

        game = Label(admin)
        game["text"] = "Game: " + str(self.gameNumber)
        game.grid(row=0, column=0, sticky=N+S+E+W)

        timeDate = Frame(admin)
        timeDate.grid(row=1, column=0)

        self.dateLbl = Label(timeDate, text="Date: ").grid(row=0, column=0)
        self.dateVar = StringVar()
        self.dateField = Entry(timeDate, textvariable=self.dateVar).grid(row=0, column=1)
        currentDate = str(datetime.date.today().day) + "/" + str(datetime.date.today().month) + "/" + str(datetime.date.today().year)
        self.dateVar.set(currentDate)

        self.timeLbl = Label(timeDate, text="Time: ").grid(row=1, column=0)
        self.timeVar = StringVar()
        self.timeEntry = Entry(timeDate, textvariable=self.timeVar).grid(row=1, column=1)
        self.gameStart = datetime.datetime.now().time()
        self.timeVar.set(str(self.gameStart).split()[0][:-10])

        self.resultLbl = Label(timeDate)
        self.resultLbl["text"] = "Result: "+str(self.team1score)+"v"+str(self.team2score)
        self.resultLbl.grid(row=0, column=2)
        
        self.shootoutLbl = Label(timeDate, text="Shootout: v").grid(row=1, column=2)
        self.finalLbl = Label(timeDate, text="Final: v").grid(row=2, column=2)
        
        self.ref1Lbl = Label(timeDate, text="Ref1").grid(row=0, column=4)
        self.ref1Var = StringVar()
        self.ref1 = Entry(timeDate, textvariable=self.ref1Var).grid(row=0, column=5)
        self.ref1Var.set("Referee 1")

        self.ref2Lbl = Label(timeDate, text="Ref2").grid(row=1, column=4)
        self.ref2Var = StringVar()
        self.ref2 = Entry(timeDate, textvariable=self.ref2Var).grid(row=1, column=5)
        self.ref2Var.set("Referee 2")

        self.scorerLbl = Label(timeDate, text="Scorer").grid(row=0, column=6)
        self.scorerVar = StringVar()
        self.scorerFld = Entry(timeDate, textvariable=self.scorerVar).grid(row=0, column=7)
        self.scorerVar.set("Scorer")

        self.timekeeperLbl = Label(timeDate, text="Timekeeper").grid(row=1, column=6)
        self.timekeeperVar = StringVar()
        self.timekeeperFld = Entry(timeDate, textvariable=self.timekeeperVar).grid(row=1, column=7)
        self.timekeeperVar.set("Timekeeper")

        ## Scoring Area
        scorer = Frame(self)
        scorer.grid(row=2, column=0)

        ## Team 1 Stuff ##
        self.team1Lab = Label(scorer)
        self.team1Lab["text"] = "Team1"
        self.team1Lab.grid(row=1, column=0)

        ## Create combobox
        self.combo = ttk.Combobox(scorer)
        self.combo.bind("<<ComboboxSelected>>", self._updatecb1)
        self.combo["values"] = (self.teamNames)
        self.combo.current(0)
        self.combo.grid(row=1, column=1)

        ## Goal Add
        self.team1goaladd = Button(scorer, width=WIDTH)
        self.team1goaladd["text"] = "+G"
        self.team1goaladd["command"] = self.team1goalUp
        self.team1goaladd.grid(row=2, column=2, sticky=S)
        ## Goal Minus
        self.team1goalmin = Button(scorer, width=WIDTH)
        self.team1goalmin["text"] = "-G"
        self.team1goalmin["command"] = self.team1goalDown
        self.team1goalmin.grid(row=2, column=3, sticky=S)
        ## Assist Add
        self.team1assadd = Button(scorer, width=WIDTH)
        self.team1assadd["text"] = "+A"
        self.team1assadd["command"] = self.team1assistUp
        self.team1assadd.grid(row=3, column=2, sticky=N)
        ## Assist Minus
        self.team1assmin = Button(scorer, width=WIDTH)
        self.team1assmin["text"] = "-A"
        self.team1assmin["command"] = self.team1assistDown
        self.team1assmin.grid(row=3, column=3, sticky=N)
        ## Saves Add
        self.team1saveadd = Button(scorer, width=WIDTH)
        self.team1saveadd["text"] = "+S"
        self.team1saveadd["command"] = self.team1ShotsOnUp
        self.team1saveadd.grid(row=4, column=2, sticky=S)
        ## Saves Minus
        self.team1savemin = Button(scorer, width=WIDTH)
        self.team1savemin["text"] = "-S"
        self.team1savemin["command"] = self.team1ShotsOnDown
        self.team1savemin.grid(row=4, column=3, sticky=S)
        ## Miss Add
        #self.team1missadd = Button(scorer, width=WIDTH)
        #self.team1missadd["text"] = "+M"
        #self.team1missadd["command"] = self.team1missesUp
        #self.team1missadd.grid(row=5, column=2, sticky=N)
        ## Miss Minus
        #self.team1missmin = Button(scorer, width=WIDTH)
        #self.team1missmin["text"] = "-M"
        #self.team1missmin["command"] = self.team1missesDown
        #self.team1missmin.grid(row=5, column=3, sticky=N)
        ## Add Minor
        self.team1addMinor = Button(scorer, width=WIDTH, text="+Minor")
        self.team1addMinor["command"] = self.team1MinorUp
        self.team1addMinor.grid(row=6, column=2)
        ## Sub Minor
        self.team1subMinor = Button(scorer, width=WIDTH, text="-Minor")
        self.team1subMinor["command"] = self.team1MinorDown
        self.team1subMinor.grid(row=6, column=3)
        ## Add Major
        self.team1addMajor = Button(scorer, width=WIDTH, text="+Major")
        self.team1addMajor["command"] = self.team1MajorUp
        self.team1addMajor.grid(row=7, column=2)
        ## Sub Major
        self.team1subMajor = Button(scorer, width=WIDTH, text="-Major")
        self.team1subMajor["command"] = self.team1MajorDown
        self.team1subMajor.grid(row=7, column=3)
        ## Add Misconduct
        self.team1addMiscon = Button(scorer, width=WIDTH, text="+Miscon")
        self.team1addMiscon["command"] = self.team1MisconUp
        self.team1addMiscon.grid(row=8, column=2)
        ## Sub Misconduct
        self.team1subMiscon = Button(scorer, width=WIDTH, text="-Miscon")
        self.team1subMiscon["command"] = self.team1MisconDown
        self.team1subMiscon.grid(row=8, column=3)
        ## Add Match
        self.team1addMatch = Button(scorer, width=WIDTH, text="+Match")
        self.team1addMatch["command"] = self.team1MatchUp
        self.team1addMatch.grid(row=9, column=2)
        ## Sub Match
        self.team1subMatch = Button(scorer, width=WIDTH, text="-Match")
        self.team1subMatch["command"] = self.team1MajorDown
        self.team1subMatch.grid(row=9, column=3)
        ## Add GameMisconduct
        self.team1addGameMis = Button(scorer, width=WIDTH, text="+GameMis")
        self.team1addGameMis["command"] = self.team1GameMisUp
        self.team1addGameMis.grid(row=10, column=2)
        ## Sub GameMisconduct
        self.team1subGameMis = Button(scorer, width=WIDTH, text="-GameMis")
        self.team1subGameMis["command"] = self.team1GameMisDown
        self.team1subGameMis.grid(row=10, column=3)

        ## Set goalie button
        self.team1setGoalie = Button(scorer, width=WIDTH, text="Set Goalie")
        self.team1setGoalie["command"] = self.team1setActGoalie
        self.team1setGoalie.grid(row=12, column=2)

        ## Create player list
        self.team1list = Listbox(scorer, height=self.maxTeamPlayers)
        for i in (player.getFullName() for player in self.team1.players):
            self.team1list.insert(END, i)
        self.team1list.grid(row=2, column=1, rowspan=9, sticky=W+E+N+S)

        ## Create goalie list
        self.team1goalieLbl = Label(scorer)
        self.team1goalieLbl["text"] = str("Goalie: " + self.team1currentGoalie.getFullName())
        self.team1goalieLbl.grid(row=11, column=1)
        self.team1goalielist = Listbox(scorer)
        for i in self.team1.players:
            if i.isGoalie:
                self.team1goalielist.insert(END, i.getFullName())
        self.team1goalielist.grid(row=12, column=1)

        ## Team 2 Stuff ##
        self.team2Lab = Label(scorer)
        self.team2Lab["text"] = "Team2"
        self.team2Lab.grid(row=1, column=3, sticky=E)

        ## Create combobox
        self.combo2 = ttk.Combobox(scorer)
        self.combo2.bind("<<ComboboxSelected>>", self._updatecb2)
        self.combo2["values"] = (self.teamNames)
        self.combo2.current(1)
        self.combo2.grid(row=1, column=4)

        ## Goal Add
        self.team2goaladd = Button(scorer, width=WIDTH)
        self.team2goaladd["text"] = "+G"
        self.team2goaladd["command"] = self.team2goalUp
        self.team2goaladd.grid(row=2, column=5, sticky=S)
        ## Goal Minus
        self.team2goalmin = Button(scorer, width=WIDTH)
        self.team2goalmin["text"] = "-G"
        self.team2goalmin["command"] = self.team2goalDown
        self.team2goalmin.grid(row=2, column=6, sticky=S)
        ## Assist Add
        self.team2assadd = Button(scorer, width=WIDTH)
        self.team2assadd["text"] = "+A"
        self.team2assadd["command"] = self.team2assistUp
        self.team2assadd.grid(row=3, column=5, sticky=N)
        ## Assist Minus
        self.team2assmin = Button(scorer, width=WIDTH)
        self.team2assmin["text"] = "-A"
        self.team2assmin["command"] = self.team2assistDown
        self.team2assmin.grid(row=3, column=6, sticky=N)
        ## Saves Add
        self.team2saveadd = Button(scorer, width=WIDTH)
        self.team2saveadd["text"] = "+S"
        self.team2saveadd["command"] = self.team2ShotsOnUp
        self.team2saveadd.grid(row=4, column=5, sticky=S)
        ## Saves Minus
        self.team2savemin = Button(scorer, width=WIDTH)
        self.team2savemin["text"] = "-S"
        self.team2savemin["command"] = self.team2ShotsOnDown
        self.team2savemin.grid(row=4, column=6, sticky=S)
        ## Miss Add
        #self.team2missadd = Button(scorer, width=WIDTH)
        #self.team2missadd["text"] = "+M"
        #self.team2missadd["command"] = self.team2missesUp
        #self.team2missadd.grid(row=5, column=5, sticky=N)
        ## Miss Minus
        #self.team2missmin = Button(scorer, width=WIDTH)
        #self.team2missmin["text"] = "-M"
        #self.team2missmin["command"] = self.team2missesDown
        #self.team2missmin.grid(row=5, column=6, sticky=N)
        ## Add Minor
        self.team2addMinor = Button(scorer, width=WIDTH, text="+Minor")
        self.team2addMinor["command"] = self.team2MinorUp
        self.team2addMinor.grid(row=6, column=5)
        ## Sub Minor
        self.team2subMinor = Button(scorer, width=WIDTH, text="-Minor")
        self.team2subMinor["command"] = self.team2MinorDown
        self.team2subMinor.grid(row=6, column=6)
        ## Add Major
        self.team2addMajor = Button(scorer, width=WIDTH, text="+Major")
        self.team2addMajor["command"] = self.team2MajorUp
        self.team2addMajor.grid(row=7, column=5)
        ## Sub Major
        self.team2subMajor = Button(scorer, width=WIDTH, text="-Major")
        self.team2subMajor["command"] = self.team2MajorDown
        self.team2subMajor.grid(row=7, column=6)
        ## Add Misconduct
        self.team2addMiscon = Button(scorer, width=WIDTH, text="+Miscon")
        self.team2addMiscon["command"] = self.team2MisconUp
        self.team2addMiscon.grid(row=8, column=5)
        ## Sub Misconduct
        self.team2subMiscon = Button(scorer, width=WIDTH, text="-Miscon")
        self.team2subMiscon["command"] = self.team2MisconDown
        self.team2subMiscon.grid(row=8, column=6)
        ## Add Match
        self.team2addMatch = Button(scorer, width=WIDTH, text="+Match")
        self.team2addMatch["command"] = self.team2MatchUp
        self.team2addMatch.grid(row=9, column=5)
        ## Sub Match
        self.team2subMatch = Button(scorer, width=WIDTH, text="-Match")
        self.team2subMatch["command"] = self.team2MatchDown
        self.team2subMatch.grid(row=9, column=6)
        ## Add GameMisconduct
        self.team2addGameMis = Button(scorer, width=WIDTH, text="+GameMis")
        self.team2addGameMis["command"] = self.team2GameMisUp
        self.team2addGameMis.grid(row=10, column=5)
        ## Sub GameMisconduct
        self.team2subGameMis = Button(scorer, width=WIDTH, text="-GameMis")
        self.team2subGameMis["command"] = self.team2GameMisDown
        self.team2subGameMis.grid(row=10, column=6)

        ## Set goalie button
        self.team2setGoalie = Button(scorer, width=WIDTH, text="Set Goalie")
        self.team2setGoalie["command"] = self.team2setActGoalie
        self.team2setGoalie.grid(row=12, column=5)

        ## Create player list
        self.team2list = Listbox(scorer, height=self.maxTeamPlayers)
        for i in (player.getFullName() for player in self.team2.players):
            self.team2list.insert(END, i)
        self.team2list.grid(row=2, column=4, rowspan=9, sticky=W+E+N+S)

        ## Create goalie list
        self.team2goalieLbl = Label(scorer)
        self.team2goalieLbl["text"] = str("Goalie: " + self.team2currentGoalie.getFullName())
        self.team2goalieLbl.grid(row=11, column=4)
        self.team2goalielist = Listbox(scorer)
        for i in self.team2.players:
            if i.isGoalie:
                self.team2goalielist.insert(END, i.getFullName())
        self.team2goalielist.grid(row=12, column=4)

        ## End Game Button
        self.endGame = Button(self)
        self.endGame["text"] = "End Game"
        self.endGame["command"] = self.endGameProc
        self.endGame.grid(row=3, column=0, sticky=N+S+E+W)

    def team1setActGoalie(self):
        playerIndex = self.team1goalielist.curselection()[0]
        self.team1currentGoalie = self.team1.players[int(playerIndex)]
        self.actions.append("-" + self.team1currentGoalie.getFullName() + " is the active goalie")
        self.team1goalieLbl["text"]=str("Goalie: " + self.team1currentGoalie.getFullName())

    def team2setActGoalie(self):
        playerIndex = self.team2goalielist.curselection()[0]
        self.team2currentGoalie = self.team2.players[int(playerIndex)]
        self.actions.append("-" + self.team2currentGoalie.getFullName() + " is the active goalie")
        self.team2goalieLbl["text"]=str("Goalie: " + self.team2currentGoalie.getFullName())

    def _updatecb1(self, evt):
        changedTo = evt.widget.get()

        for team in self.teamList:
            if team.teamName == changedTo:
                self.team1 = team

        self.team1list.delete(0, END)
        for i in [player.getFullName() for player in self.team1.players]:
            self.team1list.insert(END, i)

        self.team1goalielist.delete(0, END)
        for i in self.team1.players:
            if i.isGoalie:
                self.team1goalielist.insert(END, i.getFullName())

    def _updatecb2(self, evt):
        changedTo = evt.widget.get()

        for team in self.teamList:
            if team.teamName == changedTo:
                self.team2 = team

        self.team2list.delete(0, END)
        for i in [player.getFullName() for player in self.team2.players]:
            self.team2list.insert(END, i)

        self.team2goalielist.delete(0, END)
        for i in self.team2.players:
            if i.isGoalie:
                self.team2goalielist.insert(END, i.getFullName())

    def team1goalUp(self):
        self.team1score += 1
        self.resultLbl["text"] = str("Result: "+str(self.team1score)+"v"+str(self.team2score))
        playerIndex = self.team1list.curselection()[0]
        self.team1.players[int(playerIndex)].addGoal()
        self.team2currentGoalie.addShotsOn()
        self.team2currentGoalie.addMiss()
        self.actions.append("-" + self.team1.players[int(playerIndex)].getFullName() + " scored:" + str(self.team1score) + "v" + str(self.team2score))
        self.saveAllTimeData()

    def team1goalDown(self):
        self.team1score -= 1
        self.resultLbl["text"] = str("Result: "+str(self.team1score)+"v"+str(self.team2score))
        playerIndex = self.team1list.curselection()[0]
        self.team1.players[int(playerIndex)].subGoal()
        self.team2currentGoalie.subShotsOn()
        self.team2currentGoalie.subMiss()
        self.actions.append("-")
        self.saveAllTimeData()

    def team2goalUp(self):
        self.team2score += 1
        self.resultLbl["text"] = str("Result: "+str(self.team1score)+"v"+str(self.team2score))
        playerIndex = self.team2list.curselection()[0]
        self.team2.players[int(playerIndex)].addGoal()
        self.team1currentGoalie.addShotsOn()
        self.team1currentGoalie.addMiss()
        self.actions.append("-" + self.team1.players[int(playerIndex)].getFullName() + " scored:" + str(self.team1score) + "v" + str(self.team2score))
        self.saveAllTimeData()

    def team2goalDown(self):
        self.team2score -= 1
        self.resultLbl["text"] = str("Result: "+str(self.team1score)+"v"+str(self.team2score))
        playerIndex = self.team2list.curselection()[0]
        self.team1currentGoalie.subShotsOn()
        self.team1currentGoalie.subMiss()
        self.team2.players[int(playerIndex)].subGoal()
        self.actions.append("-")
        self.saveAllTimeData()

    def team1assistUp(self):
        playerIndex = self.team1list.curselection()[0]
        self.team1.players[int(playerIndex)].addAssist()
        self.actions.append("-" + self.team1.players[int(playerIndex)].getFullName() + " gained an assist")
        self.saveAllTimeData()

    def team1assistDown(self):
        playerIndex = self.team1list.curselection()[0]
        self.team1.players[int(playerIndex)].subAssist()
        self.actions.append("-")
        self.saveAllTimeData()

    def team2assistUp(self):
        playerIndex = self.team2list.curselection()[0]
        self.team2.players[int(playerIndex)].addAssist()
        self.actions.append("-" + self.team2.players[int(playerIndex)].getFullName() + " gained an assist")
        self.saveAllTimeData()

    def team2assistDown(self):
        playerIndex = self.team2list.curselection()[0]
        self.team2.players[int(playerIndex)].subAssist()
        self.actions.append("-")
        self.saveAllTimeData()

    def team1ShotsOnUp(self):
        self.team1currentGoalie.addShotsOn()
        self.actions.append("-" + self.team1currentGoalie.getFullName() + " made a save")
        self.saveAllTimeData()

    def team1ShotsOnDown(self):
        self.team1currentGoalie.subShotsOn()
        self.actions.append("-")
        self.saveAllTimeData()

    def team2ShotsOnUp(self):
        self.team2currentGoalie.addShotsOn()
        self.actions.append("-" + self.team2currentGoalie.getFullName() + " made a save")
        self.saveAllTimeData()

    def team2ShotsOnDown(self):
        self.team2currentGoalie.subShotsOn()
        self.actions.append("-")
        self.saveAllTimeData()

    #def team1missesUp(self):
    #    playerIndex = self.team1list.curselection()[0]
    #    self.team1.players[int(playerIndex)].addMiss()
    #    self.actions.append("-" + self.team1.players[int(playerIndex)].getFullName() + " was scored on")

    #def team1missesDown(self):
    #    playerIndex = self.team1list.curselection()[0]
    #    self.team1.players[int(playerIndex)].subMiss()
    #    self.actions.append("-")

    #def team2missesUp(self):
    #    playerIndex = self.team2list.curselection()[0]
    #    self.team2.players[int(playerIndex)].addMiss()
    #    self.actions.append("-" + self.team2.players[int(playerIndex)].getFullName() + " was scored on")

    #def team2missesDown(self):
    #    playerIndex = self.team2list.curselection()[0]
    #    self.team2.players[int(playerIndex)].subMiss()
    #    self.actions.append("-")

    def team1MinorUp(self):
        playerIndex = self.team1list.curselection()[0]
        self.team1.players[int(playerIndex)].addMinor()
        self.actions.append("-" + self.team1.players[int(playerIndex)].getFullName() + " gained a minor")
        self.saveAllTimeData()

    def team1MinorDown(self):
        playerIndex = self.team1list.curselection()[0]
        self.team1.players[int(playerIndex)].subMinor()
        self.actions.append("-")
        self.saveAllTimeData()

    def team1MajorUp(self):
        playerIndex = self.team1list.curselection()[0]
        self.team1.players[int(playerIndex)].addMajor()
        self.actions.append("-" + self.team1.players[int(playerIndex)].getFullName() + " gained a major")
        self.saveAllTimeData()

    def team1MajorDown(self):
        playerIndex = self.team1list.curselection()[0]
        self.team1.players[int(playerIndex)].subMajor()
        self.actions.append("-")
        self.saveAllTimeData()

    def team1MisconUp(self):
        playerIndex = self.team1list.curselection()[0]
        self.team1.players[int(playerIndex)].addMisconduct()
        self.actions.append("-" + self.team1.players[int(playerIndex)].getFullName() + " gained a misconduct penalty")
        self.saveAllTimeData()

    def team1MisconDown(self):
        playerIndex = self.team1list.curselection()[0]
        self.team1.players[int(playerIndex)].subMisconduct()
        self.actions.append("-")
        self.saveAllTimeData()

    def team1MatchUp(self):
        playerIndex = self.team1list.curselection()[0]

        ctime = datetime.datetime.now().time()
        diff = datetime.datetime.combine(datetime.date.today(), ctime) - datetime.datetime.combine(datetime.date.today(), self.gameStart)
        minutes = int(str(diff).split(":")[1])
        remainder = 48 - minutes

        self.team1.players[int(playerIndex)].addMatch(remainder)
        self.actions.append("-" + self.team1.players[int(playerIndex)].getFullName() + " gained a match penalty")
        self.saveAllTimeData()

    def team1MatchDown(self):
        playerIndex = self.team1list.curselection()[0]
        self.team1.players[int(playerIndex)].subMatch()
        self.actions.append("-")
        self.saveAllTimeData()

    def team1GameMisUp(self):
        playerIndex = self.team1list.curselection()[0]

        ctime = datetime.datetime.now().time()
        diff = datetime.datetime.combine(datetime.date.today(), ctime) - datetime.datetime.combine(datetime.date.today(), self.gameStart)
        minutes = int(str(diff).split(":")[1])
        remainder = 48 - minutes

        self.team1.players[int(playerIndex)].addGameMis(remainder)
        self.actions.append("-" + self.team1.players[int(playerIndex)].getFullName() + " gained a game misconduct penalty")
        self.saveAllTimeData()

    def team1GameMisDown(self):
        playerIndex = self.team1list.curselection()[0]
        self.team1.players[int(playerIndex)].subGameMis()
        self.actions.append("-")
        self.saveAllTimeData()

    def team2MinorUp(self):
        playerIndex = self.team1list.curselection()[0]
        self.team2.players[int(playerIndex)].addMinor()
        self.actions.append("-" + self.team2.players[int(playerIndex)].getFullName() + " gained a minor")
        self.saveAllTimeData()

    def team2MinorDown(self):
        playerIndex = self.team1list.curselection()[0]
        self.team2.players[int(playerIndex)].subMinor()
        self.actions.append("-")
        self.saveAllTimeData()

    def team2MajorUp(self):
        playerIndex = self.team1list.curselection()[0]
        self.team2.players[int(playerIndex)].addMajor()
        self.actions.append("-" + self.team2.players[int(playerIndex)].getFullName() + " gained a major")
        self.saveAllTimeData()

    def team2MajorDown(self):
        playerIndex = self.team1list.curselection()[0]
        self.team2.players[int(playerIndex)].subMajor()
        self.actions.append("-")
        self.saveAllTimeData()

    def team2MisconUp(self):
        playerIndex = self.team1list.curselection()[0]
        self.team2.players[int(playerIndex)].addMisconduct()
        self.actions.append("-" + self.team2.players[int(playerIndex)].getFullName() + " gained a misconduct penalty")
        self.saveAllTimeData()

    def team2MisconDown(self):
        playerIndex = self.team1list.curselection()[0]
        self.team2.players[int(playerIndex)].subMisconduct()
        self.actions.append("-")
        self.saveAllTimeData()

    def team2MatchUp(self):
        playerIndex = self.team1list.curselection()[0]

        ctime = datetime.datetime.now().time()
        diff = datetime.datetime.combine(datetime.date.today(), ctime) - datetime.datetime.combine(datetime.date.today(), self.gameStart)
        minutes = int(str(diff).split(":")[2].split(".")[0])
        remainder = 48 - minutes

        self.team2.players[int(playerIndex)].addMatch(remainder)
        self.actions.append("-" + self.team2.players[int(playerIndex)].getFullName() + " gained a match penalty")
        self.saveAllTimeData()

    def team2MatchDown(self):
        playerIndex = self.team1list.curselection()[0]
        self.team2.players[int(playerIndex)].subMatch()
        self.actions.append("-")
        self.saveAllTimeData()

    def team2GameMisUp(self):
        playerIndex = self.team1list.curselection()[0]

        ctime = datetime.datetime.now().time()
        diff = datetime.datetime.combine(datetime.date.today(), ctime) - datetime.datetime.combine(datetime.date.today(), self.gameStart)
        minutes = int(str(diff).split(":")[2].split(".")[0])
        remainder = 48 - minutes

        self.team2.players[int(playerIndex)].addGameMis(remainder)
        self.actions.append("-" + self.team2.players[int(playerIndex)].getFullName() + " gained a game misconduct penalty")
        self.saveAllTimeData()

    def team2GameMisDown(self):
        playerIndex = self.team1list.curselection()[0]
        self.team2.players[int(playerIndex)].subGameMis()
        self.actions.append("-")
        self.saveAllTimeData()

    def endGameProc(self):
        self.saveData()

def main():
    root = Tk()
    root.title("Scorer")
    #root.overrideredirect(1) #Uncomment to remove window borders
    app = Application(master=root)
    root.protocol('WM_DELETE_WINDOW', app.saveData)
    app.mainloop()
    root.destroy()

if __name__ == "__main__": main()