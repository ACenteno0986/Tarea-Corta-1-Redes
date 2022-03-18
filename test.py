from scipy.io import wavfile 
import IPython.display as ipd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pyaudio
import wave
import sys
from tkinter import *
#import interfaz

AudioName = "file.wav"
CHUNK = 1024

wf = wave.open("test/files/file.wav", 'rb')
p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

data = wf.readframes(CHUNK)
signal = np.frombuffer(data, dtype ="int16")
f_rate = wf.getframerate()

time = np.linspace(
        0, # start
        len(signal) / f_rate,
        num = len(signal)
    )


window = Tk()
window.title("Autrum")
window.configure(width=500, height=300)
window.configure(bg='lightgray')
canvas = FigureCanvasTkAgg(plt.figure(1), window)
plot_widget = canvas.get_tk_widget()


plot_widget.grid(row=0, column=0)


while data != b'':
    stream.write(data)
    data = wf.readframes(CHUNK)

    signal = np.frombuffer(data, dtype ="int16")
    f_rate = wf.getframerate()
    time = np.linspace(
        0, # start
        len(signal) / f_rate,
        num = len(signal)
    )
 

    plt.figure(1)
     

    plt.title("Sound Wave")
     

    plt.xlabel("Time")
    
    plt.plot(time, signal)
    
    #plt.figure(1).canvas.draw()

    #plt.show()


stream.stop_stream()
stream.close()

p.terminate()

#Audiodata = wavfile.read(AudioName)


window.mainloop()