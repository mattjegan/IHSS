from Tkinter import *
import ttk
import os

import scoreSheet
import admin

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.title = Frame(self)
        self.title.grid(row=0, column=0)

        self.photo = PhotoImage(file="Resources/ihssTitle.gif")
        self.photoLbl = Label(self.title, image=self.photo)
        self.photoLbl.image = self.photo
        self.photoLbl.grid(row=0, column=0, sticky=W)

        self.login = Frame(self)
        self.login.grid(row=1, column=0)

        self.userLbl = Label(self.login, text="Username").grid(row=0, column=0)
        self.userVar = StringVar()
        self.userFld = Entry(self.login, textvariable=self.userVar).grid(row=0, column=1)
        self.userVar.set("")

        self.passLbl = Label(self.login, text="Password").grid(row=1, column=0)
        self.passVar = StringVar()
        self.passFld = Entry(self.login, show="*", textvariable=self.passVar).grid(row=1, column=1)
        self.passVar.set("")

        self.goBtn = Button(self.login, text="Login", command=self.loginProc).grid(row=2, column=0, columnspan=2, sticky=N+S+E+W)

    def loginProc(self):
        username = self.userVar.get()
        password = self.passVar.get()

        if username == "admin" and password == "maxskate":
            os.system("python admin.py")
        elif username == "scorer" and password == "hockey":
            os.system("python scoreSheet.py")

def main():
    root = Tk()
    root.title("IHSS Login")
    root.geometry("300x200+1+1")
    app = Application(master=root)
    app.mainloop()
    root.destory()

if __name__ == "__main__": main()