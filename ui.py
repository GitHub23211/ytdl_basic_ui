import yt_dlp
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import datetime
from threading import Thread
import songq
import re


def close():
    window.destroy()

song_queue = songq.SongQ()

def download():
    x = Thread(target=start)
    x.daemon = True
    x.start()

def get_dir():
    directory = filedialog.askdirectory()
    return directory

def show_progress(dict):
    if(dict['status'] == 'downloading'):
        eta = 'Calculating...'
        name_var.set(f'Downloading: {dict["info_dict"]["title"]}')
        if(dict["eta"]):
            eta = str(datetime.timedelta(seconds=dict["eta"]))
        progress_var.set('Time Left: ' + eta)
    if(dict['status'] == 'finished'): 
        song_queue.remove()
        song_var.set(song_queue.to_string())


def pp_progress(dict):
    if(dict['status'] == 'started'):
        progress_var.set('Converting to mp3...')

def add_queue(url):
    if('https://www.youtube.com/watch' in url):
        song_to_add = re.search("^https[^&]+", url).group()
        song_queue.add(song_to_add)
        song_var.set(song_queue.to_string())
        url_txt.delete('0', 'end')

def start():
    if url_txt.get():
        add_queue(url_txt.get())
    
    filepath = get_dir()
    progress_var.set("")

    if(filepath):
        ydl_opts = {
            'format': 'm4a/bestaudio/best',
            'paths': {'home': filepath},
            'progress_hooks': [show_progress],
            'postprocessor_hooks': [pp_progress],
            'quiet': True,
            # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
            'postprocessors': [{  # Extract audio using ffmpeg
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3'
            }]
        }

        if song_queue.hasNext() == True:
            name_var.set('Starting download...')
            dl_btn['state'] = 'disabled'

            try:
                while(song_queue.hasNext()):
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        error_code = ydl.download(list(song_queue.get()))
                messagebox.showinfo("Complete", "Downloaded all files!")
            except Exception as e:
                messagebox.showerror('Error', f'Error has occurred! \n {e} with error_code {error_code}')

            name_var.set('')
            progress_var.set("Finished!")
            song_var.set('')
            dl_btn['state'] = 'normal'
            song_queue.clear()


def make_menu(w):
    global the_menu
    the_menu = tk.Menu(w, tearoff=0)
    the_menu.add_command(label="Cut")
    the_menu.add_command(label="Copy")
    the_menu.add_command(label="Paste")
    the_menu.add_command(label="Select All")

def show_menu(e):
    w = e.widget
    the_menu.entryconfigure("Cut",
    command=lambda: w.event_generate("<<Cut>>"))
    the_menu.entryconfigure("Copy",
    command=lambda: w.event_generate("<<Copy>>"))
    the_menu.entryconfigure("Paste",
    command=lambda: w.event_generate("<<Paste>>"))
    the_menu.entryconfigure("Select All",
    command=lambda: w.event_generate("<<SelectAll>>"))             
    the_menu.tk.call("tk_popup", the_menu, e.x_root, e.y_root)

# def bar():
#     progress_bar['value'] += 20

window_width = 500
window_height = 70

window = tk.Tk()
window.minsize(window_width, window_height)
window.title("YouTubeDL")

make_menu(window)

main_frame = tk.Frame(window)
url_frame = tk.Frame(main_frame)
menu_button_frame = tk.Frame(main_frame)
progress_frame = tk.Frame(main_frame)
queue_frame = tk.Frame(main_frame)

main_frame.grid()

url_frame.grid(padx=10, pady=10, sticky='w')
url_lbl = tk.Label(url_frame, text="URLS:")
url_txt = tk.Entry(url_frame, width=70)
url_lbl.grid(row=0, column=0)
url_txt.grid(row=0,column=1, ipady=5)

menu_button_frame.grid(row=1, column=0, padx=10, pady=10)
close_btn = tk.Button(menu_button_frame, text='Cancel', command=close)
dl_btn = tk.Button(menu_button_frame, text='Download', command=lambda: download())
q_btn = tk.Button(menu_button_frame, text='Add to Queue', command=lambda: add_queue(url_txt.get()))
q_btn.grid(row=1, column=1, padx=10)
dl_btn.grid(row=1, column=2, padx=10)
close_btn.grid(row=1, column=3)


progress_var = tk.StringVar(progress_frame, '', )
name_var = tk.StringVar(progress_frame, '', )
song_var = tk.StringVar(queue_frame, '')
#progress_bar = ttk.Progressbar(progress_frame, orient='horizontal', length=300, mode='determinate')

progress_frame.grid(row=2, column=0, padx=10, pady=10)
name_lbl = tk.Label(progress_frame, textvariable=name_var)
name_lbl.grid(row=0, column=0)
prg_lbl = tk.Label(progress_frame, textvariable=progress_var)
prg_lbl.grid(row=1, column=0)
#progress_bar.grid(row=2, column=0)

queue_frame.grid(row=3, column=0, padx=10, pady=10)
q_lbl = tk.Label(queue_frame, text='Song Queue')
q_lbl.grid(row=0, column=0)
songq_lbl = tk.Label(queue_frame, textvariable=song_var)
songq_lbl.grid(row=1, column=0)

url_txt.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_menu)

window.mainloop()
