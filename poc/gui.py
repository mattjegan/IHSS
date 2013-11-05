from Tkinter import *
import ttk

class Application(Frame):
    def createWidgets(self):
        ## Create button
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"] = "red"
        self.QUIT["command"] = self.quit

        self.QUIT.grid(row=0, column=0)

        ## Team 1 Stuff ##
        self.team1Lab = Label(self)
        self.team1Lab["text"] = "Team1"
        self.team1Lab.grid(row=1, column=0)

        ## Create combobox
        self.combo = ttk.Combobox(self)
        self.combo.bind("<<ComboboxSelected>>", self._update)
        self.combo["values"] = (1, 2, 3)
        self.combo.grid(row=1, column=1)

        ## Goal Add
        self.team1goaladd = Button(self, width=5)
        self.team1goaladd["text"] = "+G"
        self.team1goaladd.grid(row=2, column=2, sticky=S)
        ## Goal Minus
        self.team1goalmin = Button(self, width=5)
        self.team1goalmin["text"] = "-G"
        self.team1goalmin.grid(row=2, column=3, sticky=S)
        ## Assist Add
        self.team1assadd = Button(self, width=5)
        self.team1assadd["text"] = "+A"
        self.team1assadd.grid(row=3, column=2)
        ## Assist Minus
        self.team1assmin = Button(self, width=5)
        self.team1assmin["text"] = "-A"
        self.team1assmin.grid(row=3, column=3)
        ## Saves Add
        self.team1saveadd = Button(self, width=5)
        self.team1saveadd["text"] = "+S"
        self.team1saveadd.grid(row=4, column=2, sticky=N)
        ## Saves Minus
        self.team1savemin = Button(self, width=5)
        self.team1savemin["text"] = "-S"
        self.team1savemin.grid(row=4, column=3, sticky=N)

        ## Create player list
        self.team1list = Listbox(self)
        for i in [1, 2, 3]:
            self.team1list.insert(END, i)
        self.team1list.grid(row=2, column=1, rowspan=3, sticky=W+E+N+S)

        ## Team 2 Stuff ##
        self.team2Lab = Label(self)
        self.team2Lab["text"] = "Team2"
        self.team2Lab.grid(row=1, column=3, sticky=E)

        ## Create combobox
        self.combo2 = ttk.Combobox(self)
        self.combo2.bind("<<ComboboxSelected>>", self._update)
        self.combo2["values"] = (1, 2, 3)
        self.combo2.grid(row=1, column=4)

        ## Goal Add
        self.team2goaladd = Button(self, width=5)
        self.team2goaladd["text"] = "+G"
        self.team2goaladd.grid(row=2, column=5, sticky=S)
        ## Goal Minus
        self.team2goalmin = Button(self, width=5)
        self.team2goalmin["text"] = "-G"
        self.team2goalmin.grid(row=2, column=6, sticky=S)
        ## Assist Add
        self.team2assadd = Button(self, width=5)
        self.team2assadd["text"] = "+A"
        self.team2assadd.grid(row=3, column=5)
        ## Assist Minus
        self.team2assmin = Button(self, width=5)
        self.team2assmin["text"] = "-A"
        self.team2assmin.grid(row=3, column=6)
        ## Saves Add
        self.team2saveadd = Button(self, width=5)
        self.team2saveadd["text"] = "+S"
        self.team2saveadd.grid(row=4, column=5, sticky=N)
        ## Saves Minus
        self.team2savemin = Button(self, width=5)
        self.team2savemin["text"] = "-S"
        self.team2savemin.grid(row=4, column=6, sticky=N)

        ## Create player list
        self.team2list = Listbox(self)
        for i in [1, 2, 3]:
            self.team2list.insert(END, i)
        self.team2list.grid(row=2, column=4, rowspan=3, sticky=W+E+N+S)

        ## MISC
        group = Frame(self)
        group.grid(row=5, column=0, columnspan=7)

        sep = Frame(group, height=2, width=500, borderwidth=1, relief=SUNKEN)
        sep.grid(row=0, columnspan=3)

        score1 = Label(group)
        score1["text"] = "1"
        score1.grid(row=1, column=0)

        score = Label(group)
        score["text"] = "v"
        score.grid(row=1, column=1)
        
        score2 = Label(group)
        score2["text"] = "1"
        score2.grid(row=1, column=2)


    def _update(self, evt):
        print evt.widget.get()

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()