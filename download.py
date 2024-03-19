from tkinter import StringVar, DoubleVar, filedialog, messagebox
import yt_dlp
import re
import configparser
from tkinter import Frame
from threading import Thread
from song_queue import SongQueue

class Download():
    def __init__(self, root, frame):
        self.queue = SongQueue()
        self.song_queue = StringVar(value=[])
        self.url_var = StringVar(value='')
        self.cur_dir = StringVar(value='')
        self.prog_title = StringVar(value='Ready to Download')
        self.prog_var = DoubleVar(value=0.0)
        self.save_dir = ''
        self.get_dir()
        frame(root, self).build()
    
    def get_dir(self):
        config = configparser.ConfigParser()
        config.read('dir.ini')
        self.save_dir = config['DEFAULT']['dir']
        self.cur_dir.set(value=f'Saving songs to: {self.save_dir}')
    
    def change_dir(self):
        config = configparser.ConfigParser()
        self.save_dir = filedialog.askdirectory(initialdir='./')
        config['DEFAULT'] = {
            'dir': self.save_dir
        }
        with open('dir.ini', 'w') as file:
            config.write(file)
            file.close()
        self.cur_dir.set(value=f'Saving songs to: {self.save_dir}')

    def add_song(self):
        url = self.url_var.get()
        if len(url) > 0:
            self.queue.add(url)

        self.song_queue.set(self.queue.get())
        self.url_var.set('')
    
    def dl_progress(self, dict):
        self.prog_var.set(float(dict['_percent_str'][7:12]))
    
    def pp_progress(self, dict):
        if(dict['status'] == 'started'):
            self.prog_title.set('Converting to mp3...')

    def start(self, btn):
        if self.save_dir == './' or self.save_dir is None or len(self.save_dir) == 0:
            try:
                self.change_dir()
            except Exception as e:
                messagebox.showerror('Error', 'Invalid save location')
        
        x = Thread(target=lambda: self.download_queue(btn))
        x.daemon = True

        self.prog_title.set('Downloading...')
        btn.config(state='disabled')

        x.start()
    
    def download_queue(self, btn):
        opts = {
            'format': 'bestaudio/best',
            # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
            'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128'
        }],
            'paths': {'home': self.save_dir},
            'progress_hooks': [self.dl_progress],
            'postprocessor_hooks': [self.pp_progress],
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(opts) as yt:
            yt.download(self.queue.get())
        
        messagebox.showinfo('Finished', 'Finished!')
        btn.config(state='normal')
        self.reset_progress()

    def reset_progress(self):
        self.prog_title = StringVar(value='Ready to Download')
        self.prog_var = DoubleVar(value=0.0)