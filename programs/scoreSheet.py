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
        self.loadData()
        self.gameNumber = int([line for line in open("gameNumber.txt", "rU")][0])
        self.teamNames = []
        for team in self.teamList:
            self.teamNames.append(team.teamName)
        self.team1 = self.teamList[0]
        self.team2 = self.teamList[1]
        self.team1score = 0
        self.team2score = 0
        self.createWidgets()

    def addTeam(self, team):
        self.teamList.append(team)

    def loadData(self):
        dataFile = open("teamData.txt", "rU")
        dataArray = [line for line in dataFile]
        dataFile.close()

        teams = []
        currentTeam = -1

        for item in dataArray:
            if str(item)[0] != '-':
                currentTeam += 1
                newTeam = teamClass.Team(str(item).strip())
                teams.append(newTeam)
            else:
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

        gameFile.write(self.team1.teamName)
        for player in self.team1.players:
            gameFile.write("\n")
            gameFile.write(player.saveData(True))

        gameFile.write("\n")

        gameFile.write(self.team2.teamName)
        for player in self.team2.players:
            gameFile.write("\n")
            gameFile.write(player.saveData(True))

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

    def createWidgets(self):
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
        currentTime = str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute)
        self.timeVar.set(currentTime)

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
        self.team1goaladd = Button(scorer, width=5)
        self.team1goaladd["text"] = "+G"
        self.team1goaladd["command"] = self.team1goalUp
        self.team1goaladd.grid(row=2, column=2, sticky=S)
        ## Goal Minus
        self.team1goalmin = Button(scorer, width=5)
        self.team1goalmin["text"] = "-G"
        self.team1goalmin["command"] = self.team1goalDown
        self.team1goalmin.grid(row=2, column=3, sticky=S)
        ## Assist Add
        self.team1assadd = Button(scorer, width=5)
        self.team1assadd["text"] = "+A"
        self.team1assadd["command"] = self.team1assistUp
        self.team1assadd.grid(row=3, column=2, sticky=N)
        ## Assist Minus
        self.team1assmin = Button(scorer, width=5)
        self.team1assmin["text"] = "-A"
        self.team1assmin["command"] = self.team1assistDown
        self.team1assmin.grid(row=3, column=3, sticky=N)
        ## Saves Add
        self.team1saveadd = Button(scorer, width=5)
        self.team1saveadd["text"] = "+S"
        self.team1saveadd["command"] = self.team1ShotsOnUp
        self.team1saveadd.grid(row=4, column=2, sticky=S)
        ## Saves Minus
        self.team1savemin = Button(scorer, width=5)
        self.team1savemin["text"] = "-S"
        self.team1savemin["command"] = self.team1ShotsOnDown
        self.team1savemin.grid(row=4, column=3, sticky=S)
        ## Miss Add
        self.team1missadd = Button(scorer, width=5)
        self.team1missadd["text"] = "+M"
        self.team1missadd["command"] = self.team1missesUp
        self.team1missadd.grid(row=5, column=2, sticky=N)
        ## Miss Minus
        self.team1missmin = Button(scorer, width=5)
        self.team1missmin["text"] = "-M"
        self.team1missmin["command"] = self.team1missesDown
        self.team1missmin.grid(row=5, column=3, sticky=N)

        ## Create player list
        self.team1list = Listbox(scorer, height=15)
        for i in (player.getFullName() for player in self.team1.players):
            self.team1list.insert(END, i)
        self.team1list.grid(row=2, column=1, rowspan=4, sticky=W+E+N+S)

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
        self.team2goaladd = Button(scorer, width=5)
        self.team2goaladd["text"] = "+G"
        self.team2goaladd["command"] = self.team2goalUp
        self.team2goaladd.grid(row=2, column=5, sticky=S)
        ## Goal Minus
        self.team2goalmin = Button(scorer, width=5)
        self.team2goalmin["text"] = "-G"
        self.team2goalmin["command"] = self.team2goalDown
        self.team2goalmin.grid(row=2, column=6, sticky=S)
        ## Assist Add
        self.team2assadd = Button(scorer, width=5)
        self.team2assadd["text"] = "+A"
        self.team2assadd["command"] = self.team2assistUp
        self.team2assadd.grid(row=3, column=5, sticky=N)
        ## Assist Minus
        self.team2assmin = Button(scorer, width=5)
        self.team2assmin["text"] = "-A"
        self.team2assmin["command"] = self.team2assistDown
        self.team2assmin.grid(row=3, column=6, sticky=N)
        ## Saves Add
        self.team2saveadd = Button(scorer, width=5)
        self.team2saveadd["text"] = "+S"
        self.team2saveadd["command"] = self.team2ShotsOnUp
        self.team2saveadd.grid(row=4, column=5, sticky=S)
        ## Saves Minus
        self.team2savemin = Button(scorer, width=5)
        self.team2savemin["text"] = "-S"
        self.team2savemin["command"] = self.team2ShotsOnDown
        self.team2savemin.grid(row=4, column=6, sticky=S)
        ## Miss Add
        self.team2missadd = Button(scorer, width=5)
        self.team2missadd["text"] = "+M"
        self.team2missadd["command"] = self.team2missesUp
        self.team2missadd.grid(row=5, column=5, sticky=N)
        ## Miss Minus
        self.team2missmin = Button(scorer, width=5)
        self.team2missmin["text"] = "-M"
        self.team2missmin["command"] = self.team2missesDown
        self.team2missmin.grid(row=5, column=6, sticky=N)

        ## Create player list
        self.team2list = Listbox(scorer, height=15)
        for i in (player.getFullName() for player in self.team2.players):
            self.team2list.insert(END, i)
        self.team2list.grid(row=2, column=4, rowspan=4, sticky=W+E+N+S)

        ## End Game Button
        self.endGame = Button(self)
        self.endGame["text"] = "End Game"
        self.endGame["command"] = self.endGameProc
        self.endGame.grid(row=3, column=0, sticky=N+S+E+W)

    def _updatecb1(self, evt):
        changedTo = evt.widget.get()

        for team in self.teamList:
            if team.teamName == changedTo:
                self.team1 = team

        self.team1list.delete(0, END)
        for i in [player.getFullName() for player in self.team1.players]:
            self.team1list.insert(END, i)

    def _updatecb2(self, evt):
        changedTo = evt.widget.get()

        for team in self.teamList:
            if team.teamName == changedTo:
                self.team2 = team

        self.team2list.delete(0, END)
        for i in [player.getFullName() for player in self.team2.players]:
            self.team2list.insert(END, i)

    def team1goalUp(self):
        self.team1score += 1
        self.resultLbl["text"] = str("Result: "+str(self.team1score)+"v"+str(self.team2score))
        playerIndex = self.team1list.curselection()[0]
        self.team1.players[int(playerIndex)].addGoal()

    def team1goalDown(self):
        self.team1score -= 1
        self.resultLbl["text"] = str("Result: "+str(self.team1score)+"v"+str(self.team2score))
        playerIndex = self.team1list.curselection()[0]
        self.team1.players[int(playerIndex)].subGoal()

    def team2goalUp(self):
        self.team2score += 1
        self.resultLbl["text"] = str("Result: "+str(self.team1score)+"v"+str(self.team2score))
        playerIndex = self.team2list.curselection()[0]
        self.team2.players[int(playerIndex)].addGoal()

    def team2goalDown(self):
        self.team2score -= 1
        self.resultLbl["text"] = str("Result: "+str(self.team1score)+"v"+str(self.team2score))
        playerIndex = self.team2list.curselection()[0]
        self.team2.players[int(playerIndex)].subGoal()

    def team1assistUp(self):
        playerIndex = self.team1list.curselection()[0]
        self.team1.players[int(playerIndex)].addAssist()

    def team1assistDown(self):
        playerIndex = self.team1list.curselection()[0]
        self.team1.players[int(playerIndex)].subAssist()

    def team2assistUp(self):
        playerIndex = self.team2list.curselection()[0]
        self.team2.players[int(playerIndex)].addAssist()

    def team2assistDown(self):
        playerIndex = self.team2list.curselection()[0]
        self.team2.players[int(playerIndex)].subAssist()

    def team1ShotsOnUp(self):
        playerIndex = self.team1list.curselection()[0]
        self.team1.players[int(playerIndex)].addShotsOn()

    def team1ShotsOnDown(self):
        playerIndex = self.team1list.curselection()[0]
        self.team1.players[int(playerIndex)].subShotsOn()

    def team2ShotsOnUp(self):
        playerIndex = self.team2list.curselection()[0]
        self.team2.players[int(playerIndex)].addShotsOn()

    def team2ShotsOnDown(self):
        playerIndex = self.team2list.curselection()[0]
        self.team2.players[int(playerIndex)].subShotsOn()

    def team1missesUp(self):
        playerIndex = self.team1list.curselection()[0]
        self.team1.players[int(playerIndex)].addMiss()

    def team1missesDown(self):
        playerIndex = self.team1list.curselection()[0]
        self.team1.players[int(playerIndex)].subMiss()

    def team2missesUp(self):
        playerIndex = self.team2list.curselection()[0]
        self.team2.players[int(playerIndex)].addMiss()

    def team2missesDown(self):
        playerIndex = self.team2list.curselection()[0]
        self.team2.players[int(playerIndex)].subMiss()

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