from tkinter import ttk, Frame, Label, Entry, Button, Listbox, Scrollbar, StringVar, DoubleVar, messagebox, filedialog, ttk
import datetime

class UI(Frame):
    def __init__(self, root, state):
        Frame.__init__(self, root)
        self.url_var = StringVar(value='')
        self.prog_title = StringVar(value='Ready to Download')
        self.prog_var = DoubleVar(value=0.0)
        self.song_queue = StringVar(value=state.queue.get())
        root.columnconfigure(0, weight=1)
    
    def build(self):
        self.grid()
        self.url_entry()
        self.buttons()
        self.progress_bar()
        self.song_list()

    def url_entry(self):
        f = Frame(self)
        url_lbl = Label(f, text='URL:')
        url_ent = Entry(f, textvariable=self.url_var, width=50)

        f.grid(padx=10, pady=20)
        url_lbl.grid(row=0, column=0)
        url_ent.grid(row=0, column=1)
    
    def buttons(self):
        f = Frame(self)

        add_song = Button(f, text='Add to Queue')
        download = Button(f, text='Start Download')
        cancel = Button(f, text='Cancel')

        f.grid()
        add_song.grid(row=0, column=0, padx=10, sticky=('w', 'e'))
        download.grid(row=0, column=1, sticky=('w', 'e'))
        cancel.grid(row=0, column=2, padx=10, sticky=('w', 'e'))
    
    def progress_bar(self):
        f = Frame(self)
        t = Label(f, textvariable=self.prog_title)
        p = ttk.Progressbar(f, orient='horizontal', length=300, mode='determinate', variable=self.prog_var, value=self.prog_var.get())

        f.grid(pady=20)
        t.grid()
        p.grid()

    
    def song_list(self):
        f = Frame(self)
        title = Label(f, text='Song Queue')
        lbox = Listbox(f, width=61, listvariable=self.song_queue, selectmode='single', state='disabled')
        scroll = Scrollbar(f, orient='vertical', command=lbox.yview)
        lbox.configure(yscrollcommand=scroll.set)

        f.grid(pady=20)
        title.grid(row=0, column=0)
        lbox.grid(row=1, column=0)
        scroll.grid(row=1, column=1, sticky=('n', 's'))