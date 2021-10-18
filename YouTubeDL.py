import youtube_dl
import tkinter as tk
from tkinter import ttk
import re

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
dl_vid = tk.Checkbutton(options_frame, text='Download Video')
dl_audio = tk.Checkbutton(options_frame, text='Download Audio')
dl_vid.grid(row=1)
dl_audio.grid(row=2, pady=10)

quality_frame.grid(row=1, column=0, padx=50)
string_var = tk.StringVar(quality_frame, 'Select Quality...')
audq_cmb = ttk.Combobox(quality_frame, textvariable=string_var, state='readonly', width=30)
vidq_cmb = ttk.Combobox(quality_frame, textvariable=string_var, state='readonly', width=30)
audq_cmb.grid(row=1, column=2, sticky='e')
vidq_cmb.grid(row=2, column=2, pady=10)

progress_frame.grid(row=2, column=0, sticky='w', padx=15)
prog_lbl = tk.Label(progress_frame, text='Progress:')
prog_bar = ttk.Progressbar(progress_frame, orient='horizontal', length=450, mode='determinate')
prog_lbl.grid(row=2, column=0, sticky='w')
prog_bar.grid(row=3, column=0)

menu_button_frame.grid(row=5, column=0, sticky='e')
dl_btn = ttk.Button(menu_button_frame, text='Download')
close_btn = ttk.Button(menu_button_frame, text='Close')
dl_btn.grid(row=5, column=0)
close_btn.grid(row=5, column=1, padx=10)

window.mainloop()

# ytdl = youtube_dl.YoutubeDL({
#             'format': '140',
#             'restrictfilenames': True,
#             'extract_flat': True,
#             'noplaylist': True,
#             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#             'source_address': '0.0.0.0'
# })

# #url = input("URL of video you want to download?\n")

# ytdl.extract_info(url, download=True)


