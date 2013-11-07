from Tkinter import *
import ttk

import teamClass
import playerClass

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.teamList = []
        self.pack()
        self.loadData()
        self.teamNames = []
        for team in self.teamList:
            self.teamNames.append(team.teamName)
        self.team1 = self.teamList[0]
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
                # (self, firstName, lastName, number, isGoalie=False)
                playerData = [part for part in item.strip().split(';')]
                playerData[0] = playerData[0][1:]
                if int(playerData[6]) == 0:
                    playerData[6] = False
                else:
                    playerData[6] = True
                newPlayer = playerClass.Player(playerData[0], playerData[1], int(playerData[2]), int(playerData[3]), int(playerData[4]), int(playerData[5]), int(playerData[6]))
                # Assign to team
                teams[currentTeam].addPlayer(newPlayer)

        for team in teams:
            self.addTeam(team)

    #def saveData(self):
    #    teamData = []
    #    for team in self.teamList:
    #        teamData.append(team.teamName)
    #        for player in team.players:
    #            teamData.append(player.saveData())

    #    self.quit()
    #    dataFile = open("teamData.txt", "w")
    #    for item in teamData:
    #        dataFile.write(item + "\n")
    #    dataFile.close()

    def createWidgets(self):
        ## Team Stuff ##
        self.team1Lab = Label(self)
        self.team1Lab["text"] = "Team"
        self.team1Lab.grid(row=1, column=0)

        ## Create combobox
        self.combo = ttk.Combobox(self)
        self.combo.bind("<<ComboboxSelected>>", self._updatecb1)
        self.combo["values"] = (self.teamNames)
        self.combo.current(0)
        self.combo.grid(row=1, column=1)

        ## Add Player
        self.addPlayer = Button(self, width=20)
        self.addPlayer["text"] = "Add Player"
        #self.addPlayer["command"] = self.addPlayerCom
        self.addPlayer.grid(row=2, column=2, sticky=S)

        ## Delete Player
        self.delPlayer = Button(self, width=20)
        self.delPlayer["text"] = "Delete Player"
        self.delPlayer["command"] = self.delPlayerCom
        self.delPlayer.grid(row=3, column=2, sticky=S)

        ## Add Team
        self.addTeamBtn = Button(self, width=20)
        self.addTeamBtn["text"] = "Add Team"
        #self.addTeamBtn["command"] = self.addTeamCom
        self.addTeamBtn.grid(row=4, column=2, sticky=S)

        ## Delete Team
        self.delTeamBtn = Button(self, width=20)
        self.delTeamBtn["text"] = "Delete Team"
        #self.delTeamBtn["command"] = self.delTeamCom
        self.delTeamBtn.grid(row=5, column=2, sticky=S)

        ## Create player list
        self.team1list = Listbox(self)
        for i in (player.getFullName() for player in self.team1.players):
            self.team1list.insert(END, i)
        self.team1list.grid(row=2, column=1, rowspan=4, sticky=W+E+N+S)

    def _updatecb1(self, evt):
        changedTo = evt.widget.get()

        for team in self.teamList:
            if team.teamName == changedTo:
                self.team1 = team

        self.team1list.delete(0, END)
        for i in [player.getFullName() for player in self.team1.players]:
            self.team1list.insert(END, i)

    def addPlayerCom(self):
        ## Create new dialog window for entry
        pass

    def delPlayerCom(self):
        try:
            playerIndex = self.team1list.curselection()[0]
            print "Deleting:", self.team1.players[int(playerIndex)].getFullName()
            self.team1list.delete(int(playerIndex))
            self.team1.players.remove(self.team1.players[int(playerIndex)])
        except:
            pass

    def addTeamCom(self):
        ## Create new dialog window for entry
        pass

    def delTeamCom(self):
        pass

def main():
    root = Tk()
    root.title("Scorer")
    #root.overrideredirect(1) #Uncomment to remove window borders
    app = Application(master=root)
    #root.protocol('WM_DELETE_WINDOW', app.saveData)
    app.mainloop()
    root.destroy()

if __name__ == "__main__": main()