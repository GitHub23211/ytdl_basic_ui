import youtube_dl
import tkinter as tk
from tkinter import ttk
import re
from threading import Thread

ytdl_opts = {
    'extract_flat': True,
    'noplaylist': True,
}
ytdl = youtube_dl.YoutubeDL(ytdl_opts)

def close():
    window.destroy()


def get_formats():
    audio_formats = []
    video_formats = []
    info = ytdl.extract_info(url_ent.get(), download=False)
    for form in info['formats']:
        if 'audio' in form['format']:
            audio_formats.append(str(form['format']) + " " + str(form['asr']) + "Hz")
        else:
            video_formats.append(form['format']) 
    vidq_cmb['values'] = video_formats
    audq_cmb['values'] = audio_formats
    url_ent.configure(state='readonly')

def download():
    x = Thread(target=start)
    x.daemon = True
    x.start()

def start():
    global aud_bool
    global vid_bool
    if aud_bool.get() and vid_bool.get():
        aud_id = re.search(r'(?P<audq>.*?)-', audq_cmb.get(), re.IGNORECASE)
        vid_id = re.search(r'(?P<vidq>.*?)-', vidq_cmb.get(), re.IGNORECASE)
        ytdl_opts['formats'] = [aud_id.group('audq'), vid_id.group('vidq')]
    elif vid_bool.get():
        vid_id = re.search(r'(?P<vidq>.*?)-', vidq_cmb.get(), re.IGNORECASE)
        ytdl_opts['formats'] = [vid_id.group('vidq')]
    elif aud_bool.get():
        aud_id = re.search(r'(?P<audq>.*?)-', audq_cmb.get(), re.IGNORECASE)
        ytdl_opts['formats'] = [aud_id.group('audq')]
    else:
        print("Check a box")
        return 0
    ytdl = youtube_dl.YoutubeDL(ytdl_opts)
    ytdl.extract_info(url_ent.get(), download=True)


window_width = 500
window_height = 400

window = tk.Tk()
window.minsize(window_width, window_height)
window.title("YouTubeDL")

main_frame = tk.Frame(window)
url_frame = tk.Frame(main_frame)
options_frame = tk.Frame(main_frame)
quality_frame = tk.Frame(main_frame)
progress_frame = tk.Frame(main_frame)
empty_frame = tk.Frame(window, width=window_width, height=200)
menu_button_frame = tk.Frame(window)

main_frame.grid()
empty_frame.grid(row=4, column=0, )

url_frame.grid(padx=10, pady=10, sticky='w')
url_lbl = tk.Label(url_frame, text="URL:")
url_ent = tk.Entry(url_frame, width=70)
url_lbl.grid(row=0, column=0)
url_ent.grid(row=0,column=1)

options_frame.grid(row=1, padx=10, sticky='w')
aud_bool = tk.BooleanVar(False)
vid_bool = tk.BooleanVar(False)
dl_vid = tk.Checkbutton(options_frame, text='Download Video', variable=vid_bool, onvalue=True, offvalue=False)
dl_audio = tk.Checkbutton(options_frame, text='Download Audio', variable=aud_bool, onvalue=True, offvalue=False)
dl_vid.grid(row=1)
dl_audio.grid(row=2, pady=10)

quality_frame.grid(row=1, column=0, padx=50, sticky='e')
vid_string = tk.StringVar(quality_frame, 'Select Quality...')
aud_string = tk.StringVar(quality_frame, 'Select Quality...')
audq_cmb = ttk.Combobox(quality_frame, textvariable=vid_string, state='readonly', width=40)
vidq_cmb = ttk.Combobox(quality_frame, textvariable=aud_string, state='readonly', width=40)
vidq_cmb.grid(row=1, column=1, sticky='e')
audq_cmb.grid(row=2, column=1, pady=10)

progress_frame.grid(row=2, column=0, sticky='w', padx=15)
prog_lbl = tk.Label(progress_frame, text='Progress:')
prog_bar = ttk.Progressbar(progress_frame, orient='horizontal', length=450, mode='determinate')
prog_lbl.grid(row=2, column=0, sticky='w')
prog_bar.grid(row=3, column=0)

menu_button_frame.grid(row=5, column=0, sticky='e')
format_btn = ttk.Button(menu_button_frame, text='Get Formats', command=get_formats)
close_btn = ttk.Button(menu_button_frame, text='Close', command=close)
dl_btn = ttk.Button(menu_button_frame, text='Download', command=download)
format_btn.grid(row=5, column=0)
dl_btn.grid(row=5, column=1, padx=10)
close_btn.grid(row=5, column=2, padx=10)

window.mainloop()

