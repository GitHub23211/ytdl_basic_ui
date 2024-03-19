from tkinter import Tk
from download import Download
from ui import UI

class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.minsize(500, 70)
        self.title('YouTubeDL')
        Download(self, UI)



if __name__ == '__main__':
    app = App()
    app.mainloop()