from tkinter import ttk, Frame, Label, Entry, Button, Listbox, Scrollbar, Menu, ttk

class UI(Frame):
    def __init__(self, root, state):
        Frame.__init__(self, root)
        self.state = state
        self.menu = Menu(self, tearoff=0)
        root.columnconfigure(0, weight=1)
    
    def build(self):
        self.grid()
        self.make_menu()
        self.url_entry()
        self.buttons()
        self.song_list()
        self.progress_bar()

    def url_entry(self):
        f = Frame(self)
        url_lbl = Label(f, text='URL:')
        url_ent = Entry(f, textvariable=self.state.url_var, width=50)

        url_ent.bind_class("Entry", "<Button-3><ButtonRelease-3>", self.show_menu)

        f.grid(columnspan=2, padx=10, pady=20)
        url_lbl.grid(row=0, column=0)
        url_ent.grid(row=0, column=1)
    
    def buttons(self):
        f = Frame(self)#, borderwidth=1, background='red')

        add_song = Button(f, text='Add to Queue', command=self.state.add_song)
        download = Button(f, text='Start Download', command=lambda: self.state.start(download))
        change_dir = Button(f, text='Change Directory', command=self.state.change_dir)
        rem_song = Button(f, text='Remove song', command=self.state.remove_song)
        cancel = Button(f, text='Cancel', command=self.state.interrupt_dl)

        f.grid(row=1, column=0, sticky=('w', 'e'), padx=5)
        download.grid(row=0, column=0, sticky=('w', 'e'))
        add_song.grid(row=1, column=0, sticky=('w', 'e'))
        rem_song.grid(row=2, column=0, sticky=('w', 'e'))
        change_dir.grid(row=3, column=0, sticky=('w', 'e'))
        cancel.grid(row=4, column=0, sticky=('w', 'e'))
    
    def progress_bar(self):
        f = Frame(self)
        t = Label(f, textvariable=self.state.prog_title)
        d = Label(f, textvariable=self.state.cur_dir)
        p = ttk.Progressbar(f, orient='horizontal', length=300, mode='determinate', variable=self.state.prog_var, value=self.state.prog_var.get())
        
        f.grid(columnspan=2, pady=20)
        t.grid(sticky=('e', 'w'))
        p.grid(pady=5,)
        d.grid(pady=5)
    
    def song_list(self):
        f = Frame(self)
        title = Label(f, text='Song Queue')
        lbox = Listbox(f, width=50, listvariable=self.state.song_list, selectmode='single', state='disabled')
        scroll = Scrollbar(f, orient='vertical', command=lbox.yview)
        lbox.configure(yscrollcommand=scroll.set)

        f.grid(row=1, column=1)
        title.grid(row=0, column=0)
        lbox.grid(row=1, column=0)
        scroll.grid(row=1, column=1, sticky=('n', 's'))

    def make_menu(self):
        self.menu.add_command(label="Cut")
        self.menu.add_command(label="Copy")
        self.menu.add_command(label="Paste")
        self.menu.add_command(label="Select All")

    def show_menu(self, element):
        f = element.widget
        self.menu.entryconfigure("Cut", command=lambda: f.event_generate("<<Cut>>"))
        self.menu.entryconfigure("Copy", command=lambda: f.event_generate("<<Copy>>"))
        self.menu.entryconfigure("Paste", command=lambda: f.event_generate("<<Paste>>"))
        self.menu.entryconfigure("Select All", command=lambda: f.event_generate("<<SelectAll>>"))             
        self.menu.tk.call("tk_popup", self.menu, element.x_root, element.y_root)