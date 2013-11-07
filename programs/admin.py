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

    def saveData(self):
        teamData = []
        for team in self.teamList:
            teamData.append(team.teamName)
            for player in team.players:
                teamData.append(player.saveData())

        self.quit()
        dataFile = open("teamData.txt", "w")
        for item in teamData:
            dataFile.write(item + "\n")
        dataFile.close()

    def createWidgets(self):
        ## Create button

        ## Team 1 Stuff ##
        self.team1Lab = Label(self)
        self.team1Lab["text"] = "Team1"
        self.team1Lab.grid(row=1, column=0)

        ## Create combobox
        self.combo = ttk.Combobox(self)
        self.combo.bind("<<ComboboxSelected>>", self._updatecb1)
        self.combo["values"] = (self.teamNames)
        self.combo.current(0)
        self.combo.grid(row=1, column=1)

        ## Add Player
        self.addPlayer = Button(self, width=5)
        self.addPlayer["text"] = "+G"
        self.addPlayer["command"] = self.addPlayerCom
        self.addPlayer.grid(row=2, column=2, sticky=S)
        ## Delete Player
        self.delPlayer = Button(self, width=5)
        self.delPlayer["text"] = "-G"
        self.delPlayer["command"] = self.delPlayerCom
        self.delPlayer.grid(row=2, column=3, sticky=S)

        ## Create player list
        self.team1list = Listbox(self)
        for i in (player.getFullName() for player in self.team1.players):
            self.team1list.insert(END, i)
        self.team1list.grid(row=2, column=1, rowspan=3, sticky=W+E+N+S)

    def _updatecb1(self, evt):
        changedTo = evt.widget.get()

        for team in self.teamList:
            if team.teamName == changedTo:
                self.team1 = team

        self.team1list.delete(0, END)
        for i in [player.getFullName() for player in self.team1.players]:
            self.team1list.insert(END, i)

def main():
    root = Tk()
    root.title("Scorer")
    #root.overrideredirect(1) #Uncomment to remove window borders
    app = Application(master=root)
    root.protocol('WM_DELETE_WINDOW', app.saveData)
    app.mainloop()
    root.destroy()

if __name__ == "__main__": main()