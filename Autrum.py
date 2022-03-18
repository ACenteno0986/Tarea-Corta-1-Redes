from itertools import tee
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
from tkinter import simpledialog
from mutagen.mp3 import MP3
from pygame import mixer
import matplotlib.backends.backend_tkagg
import zipfile
import pyaudio
import wave
 
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 300

root = tk.ThemedTk()
root.get_themes()
root.set_theme("radiance")
root.geometry("1000x800")

statusbar = ttk.Label(root, text="Autrum", relief=SUNKEN, anchor=W, font='Times 10 italic')
statusbar.pack(side=BOTTOM, fill=X)

frame1 = Frame(root); frame1.place(x=200, y=200, width=500, height=500)
figure = plt.Figure(figsize=(5,5))
canvas = FigureCanvasTkAgg(figure, frame1)
canvas.get_tk_widget().place(x=0,y=0,width=500,height=500)
toolbar = matplotlib.backends.backend_tkagg.NavigationToolbar2Tk( canvas, root )
canvas._tkcanvas.grid(row=22,column=4)
audio = pyaudio.PyAudio()
ax = [figure.add_subplot(2, 1, 1), figure.add_subplot(2, 1, 2)]
ax[0].set_title('Grafico de freciencias y fourier')
USER_INP = ""
playlist = []
frames = []

wavFile = ""
nombreArchivo = ""
chunk = 1024

def do_plot(x, y, i, Fs):
    ax[0].clear()
    ax[0].plot(x,y)
    ax[0].axvline(x=i / Fs, color='r')
    ax[0].set_title('Grafico de freciencias y fourier')
    canvas.draw()

def do_plot2(x, y):
    ax[0].clear()
    ax[0].plot(x,y)
    canvas.draw()

def mostrar_freq():
    if(var.get == 1):
        x = np.linspace(0, CHUNK, num=CHUNK, dtype=int)
        y = np.zeros(CHUNK)
        do_plot2(x,y)

    else:
        previousTime = time.time()
        data, samplerate = sf.read(wavFile)
        sound = data
        sound = sound / 2.0**15
        signal = sound[:]

        fft_spectrum = np.fft.rfft(signal)
        freq = np.fft.rfftfreq(signal.size, d=1./samplerate)
        fft_spectrum_abs = np.abs(fft_spectrum)
        n = len(data)  
        Fs = samplerate
        time_axis = np.linspace(0, n / Fs, n, endpoint=False)
        ax[1].plot(freq[:5000], fft_spectrum_abs[:5000])

        plt.ion()
        AudiodataScaled = data/(2**15)
        spentTime = 0
        updatePeriodicity = 1

        i = 0
        while i < n:

            if paused == True:
                previousTime = time.time()
        
            else:
                if i // Fs != (i-1) // Fs:
                    spentTime += 1

                if spentTime == updatePeriodicity:

                    do_plot(time_axis,AudiodataScaled, i, Fs)
                    plt.pause(updatePeriodicity-(time.time()-previousTime))

                    previousTime = time.time()
                    spentTime = 0
                i+=1

def compressFiles(nameFile):
    file_zip = zipfile.ZipFile(nameFile+"/"+nameFile+".atm", 'w')
    for folder, subfolders, files in os.walk(nameFile):
        for file in files:
            if not file.endswith('.atm'):
                file_zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), nameFile), compress_type = zipfile.ZIP_DEFLATED)
    file_zip.close()


def extractFiles(filename_path):
    name = os.path.basename(filename_path).split(".")
    file_zip = zipfile.ZipFile(filename_path)
    file_zip.extractall(name[0]+"/"+name[0]+"Data")
    file_zip.close()
    return name[0]

def browse_file():
    global filename_path
    global wavFile
    filename_path = filedialog.askopenfilename()
    name = extractFiles(filename_path)
    nameFolder=name+"/"+name+"Data"
    for folder, subfolders, files in os.walk(nameFolder):
        for file in files:
            if file.endswith('.wav'):
                wavFile = os.path.basename(file)
                text = StringVar()
                text.set(os.path.basename(filename_path))
                label.config(textvariable=text)
                mixer.music.queue(wavFile)

mixer.init()

root.title("Autrum")

leftframe = Frame(root)
leftframe.pack(side=LEFT, padx=30, pady=30)

label = Label(leftframe, text="Seleccione un archivo...")
label.pack()

addBtn = ttk.Button(leftframe, text="Cargar archivo", command=browse_file)
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

    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()
    p2 = threading.Thread(target=mostrar_freq, args=())
    p2.start()


def start_count(t):
    global paused
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            time.sleep(1)
            current_time += 1

def reproducir():
    global paused
    
    if(var.get() == 0):
        if paused:
            mixer.music.unpause()
            statusbar['text'] = "Reproduciendo..."
            paused = FALSE
        else:
            try:
                stop_music()
                time.sleep(1)
                mixer.music.load(wavFile)
                mixer.music.play()
                statusbar['text'] = "Reproduciendo" + ' - ' + os.path.basename(wavFile)
                show_details(wavFile)
            except:
                tkinter.messagebox.showerror('Error al abrir o cargar el archivo')

    if(var.get() == 1):
        print("Prua de que entra a grabar")
        p3 = threading.Thread(target=grabar, args=())
        p3.start()       

def grabar():
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
        
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        if(terminar == True):
            stream.stop_stream()
            stream.close()
            audio.terminate()

        else:
            data = stream.read(CHUNK)
            frames.append(data)
 
    stream.stop_stream()
    stream.close()
    audio.terminate()

def stop_music():
    mixer.music.stop()

def terminar():
    global terminar
    terminar = True
    if(var.get() == 1):
        USER_INP = simpledialog.askstring(title="Nombre",
                                  prompt="Escriba el nombre del archivo")
        
        os.mkdir(USER_INP)
        waveFile = wave.open(USER_INP + "/" + USER_INP + ".wav", 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        compressFiles(USER_INP)

paused = FALSE

def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused"

var = IntVar()
checkbox = ttk.Checkbutton(root, text="Modo Grabacion", variable=var, onvalue=1, offvalue=0,)
checkbox.place(x=10, y=10)

middleframe = Frame(rightframe)
middleframe.pack(pady=30, padx=30)

playBtn = ttk.Button(middleframe, text="Reproducir/Grabar", command=reproducir)
playBtn.grid(row=0, column=0, padx=10)

pauseBtn = ttk.Button(middleframe, text="Pausar", command=pause_music)
pauseBtn.grid(row=0, column=1, padx=10)

stopBtn = ttk.Button(middleframe, text="Parar", command=stop_music)
stopBtn.grid(row=0, column=2, padx=10)

stopBtn = ttk.Button(middleframe, text="Terminar", command=terminar)
stopBtn.grid(row=0, column=3, padx=10)

bottomframe = Frame(rightframe)
bottomframe.pack()

def on_closing():
    stop_music()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()