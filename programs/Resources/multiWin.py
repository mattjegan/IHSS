from Tkinter import *
import ttk

def main():
    root = Tk()
    root.geometry("250x150+300+300")
    app = Application(master=root)
    app.mainloop()
    root.destroy()

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.btn = Button(self, width=20)
        self.btn["text"] = "Hello"
        self.btn["command"] = self.createNew
        self.btn.pack()

    def createNew(self):
        new = Tk()
        new.geometry("250x150+400+400")
        newa = Application(master=new)
        newa.mainloop()
        new.destroy()

if __name__ == "__main__": main()