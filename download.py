import yt_dlp
import re
from tkinter import Frame
from threading import Thread
from song_queue import SongQueue



class Download():
    def __init__(self, root, frame):
        self.queue = SongQueue()
        
        
    
        frame(root, self).build()

