import os
import threading
import time
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import themed_tk as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from mutagen.mp3 import MP3
from pygame import mixer

root = tk.ThemedTk()
root.get_themes()
root.set_theme("radiance")

statusbar = ttk.Label(root, text="Autrum", relief=SUNKEN, anchor=W, font='Times 10 italic')
statusbar.pack(side=BOTTOM, fill=X)
#cv = Canvas(root, height = 300, width = 300)

frame1 = Frame(root); frame1.place(x=200, y=200, width=500, height=500)
figure = plt.Figure(figsize=(5,5))
canvas = FigureCanvasTkAgg(figure, frame1)
canvas.get_tk_widget().place(x=0,y=0,width=500,height=500)
ax = figure.add_subplot(111)

playlist = []

wavFile = "file.wav"
chunk = 1024
data, samplerate = sf.read(wavFile)
n = len(data)  # the length of the arrays contained in data
Fs = samplerate  # the sample rate
ch1 = np.array([data[[i][0]] for i in range(n)])
time_axis = np.linspace(0, n / Fs, n, endpoint=False)
sound_axis = ch1 #we only focus on the first channel here

def do_plot(x, y, i):
    ax.clear()
    ax.plot(x,y)
    ax.axvline(x=i / Fs, color='r')
    canvas.draw()



def showing_audiotrack():
    # We use a variable previousTime to store the time when a plot update is made
    # and to then compute the time taken to update the plot of the audio data.
    previousTime = time.time()

    # Turning the interactive mode on
    plt.ion()

    spentTime = 0

    # Let's the define the update periodicity
    updatePeriodicity = 1  # expressed in seconds

    # Plotting the audio data and updating the plot
    for i in range(n):
        # Each time we read one second of audio data, we increase spentTime :
        if i // Fs != (i-1) // Fs:
            spentTime += 1
        # We update the plot every updatePeriodicity seconds
        
        if spentTime == updatePeriodicity:
            

            do_plot(time_axis,sound_axis, i)
            plt.pause(updatePeriodicity-(time.time()-previousTime))

            previousTime = time.time()
            spentTime = 0

def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)

    mixer.music.queue(filename_path)


def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1

mixer.init()  # initializing the mixer

root.title("Melody")

leftframe = Frame(root)
leftframe.pack(side=LEFT, padx=30, pady=30)

playlistbox = Listbox(leftframe)
playlistbox.pack()

addBtn = ttk.Button(leftframe, text="+ Add", command=browse_file)
addBtn.pack(side=LEFT)


rightframe = Frame(root)
rightframe.pack(pady=30)

topframe = Frame(rightframe)
topframe.pack()


def show_details(play_song):
    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    # div - total_length/60, mod - total_length % 60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()
    p2 = threading.Thread(target=showing_audiotrack, args=())
    p2.start()


def start_count(t):
    global paused
    # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
    # Continue - Ignores all of the statements below it. We check if music is paused or not.
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            time.sleep(1)
            current_time += 1


def play_music():
    global paused

    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File not found', 'Melody could not find the file. Please check again.')


def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"


paused = FALSE


def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused"


middleframe = Frame(rightframe)
middleframe.pack(pady=30, padx=30)

playBtn = ttk.Button(middleframe, text="Reproducir", command=play_music)
playBtn.grid(row=0, column=0, padx=10)

stopBtn = ttk.Button(middleframe, text="Parar", command=stop_music)
stopBtn.grid(row=0, column=1, padx=10)

pauseBtn = ttk.Button(middleframe, text="Pausar", command=pause_music)
pauseBtn.grid(row=0, column=2, padx=10)

bottomframe = Frame(rightframe)
bottomframe.pack()

def on_closing():
    stop_music()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()