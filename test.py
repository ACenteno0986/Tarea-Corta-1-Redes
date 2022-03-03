#Importar Modulo scipy para leer y grabar audio
from scipy.io import wavfile 
import IPython.display as ipd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from tkinter import *

AudioName = "download.wav" # Archivo de Audio

# Salida fs: Frecuencia de muestreo and data: Señal de audio -> int16
fs, Audiodata = wavfile.read(AudioName)

plt.rcParams['figure.figsize'] = (15, 5) # Definir el tamaño de graficas

plt.plot(Audiodata) # Audiodata es un numpy array
plt.text(0-5000, np.max(Audiodata), 'Máximo', fontsize = 16,bbox=dict(facecolor='red', alpha=0.5))
plt.title('Señal de Audio sin valores adecuados en los ejes',size=16)

# declare the window
window = Tk()
# set window title
window.title("Python GUI App")
# set window width and height
window.configure(width=500, height=300)
# set window background color
window.configure(bg='lightgray')

canvas = FigureCanvasTkAgg(plt.figure(1), window)
plot_widget = canvas.get_tk_widget()
plt.figure(1).canvas.draw()


plot_widget.grid(row=0, column=0)
window.mainloop()