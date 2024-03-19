from tkinter import StringVar, DoubleVar, filedialog, messagebox
import yt_dlp
import re
import configparser
from threading import Thread
from song_queue import SongQueue

URL_REGEX = '^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu\.be))(\/(?:[\w\-]+\?v=|embed\/|live\/|v\/)?)([\w\-]+)(\S+)?$'

class Download():
    def __init__(self, root, frame):
        self.queue = SongQueue()
        self.song_queue = StringVar(value=[])
        self.url_var = StringVar(value='')
        self.cur_dir = StringVar(value='')
        self.prog_title = StringVar(value='Ready to Download')
        self.prog_var = DoubleVar(value=0.0)
        self.save_dir = ''
        self.interrupt = False
        self.regex = re.compile(URL_REGEX)
        self.get_dir()
        frame(root, self).build()
    
    def get_dir(self):
        config = configparser.ConfigParser()
        try:
            config.read('dir.ini')
            self.save_dir = config['DEFAULT']['dir']
            self.cur_dir.set(value=f'Saving songs to: {self.save_dir}')
        except KeyError as e:
            config['DEFAULT'] = {
                'dir': ''
            }
            with open('dir.ini', 'w') as file:
                config.write(file)
            self.save_dir = ''
            self.cur_dir.set(value=f'Saving songs to: {self.save_dir}')

    def change_dir(self):
        config = configparser.ConfigParser()
        new_dir = filedialog.askdirectory(initialdir='./')
        if new_dir is None or len(new_dir) == 0:
            return
        
        self.save_dir = new_dir
        config['DEFAULT'] = {
            'dir': self.save_dir
        }
        with open('dir.ini', 'w') as file:
            config.write(file)
        self.cur_dir.set(value=f'Saving songs to: {self.save_dir}')

    def add_song(self):
        url = self.url_var.get()
        if self.regex.match(url) is not None:
            self.queue.add(url)
        else:
            messagebox.showerror('Error', 'Invalid YouTube URL')

        self.song_queue.set(self.queue.get())
        self.url_var.set('')
    
    def dl_progress(self, dict):
        progress = dict['_percent_str'][7:12]
        if progress is None or len(progress) == 0:
            return
        
        self.prog_var.set(float(progress))
        if self.interrupt:
            print(self.interrupt)
            self.interrupt = False
            raise ValueError('Cancelled!')
        
        if(dict['status'] == 'finished'): 
            self.queue.remove()
            self.song_queue.set(self.queue.get())
    
    def pp_progress(self, dict):
        if(dict['status'] == 'started'):
            self.prog_title.set('Converting to mp3...')

    def start(self, btn):
        if self.save_dir == './' or self.save_dir is None or len(self.save_dir) == 0:
            try:
                self.change_dir()
            except Exception as e:
                messagebox.showerror('Error', 'Invalid save location')
        
        if not self.queue.hasNext():
            return messagebox.showerror('Error', 'No songs in queue.')
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
        try:
            while self.queue.hasNext():
                with yt_dlp.YoutubeDL(opts) as yt:
                    yt.download(self.queue.get())
            messagebox.showinfo('Finished', 'Finished!')
        except Exception as e:
            messagebox.showerror('Error', e)
        
        btn.config(state='normal')
        self.reset_progress()

    def reset_progress(self):
        self.prog_title.set(value='Ready to Download')
        self.prog_var.set(value=0.0)
    
    def interrupt_dl(self):
        self.interrupt = True