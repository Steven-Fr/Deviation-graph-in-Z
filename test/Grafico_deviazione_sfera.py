

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from sys import argv
import time


import sys
import os
from tkinter import *
import tkinter
from tkinter import messagebox
import tkinter as tk
import re
from os.path import exists

from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

from scipy.interpolate import griddata




colour = 'green3'

top = tkinter.Tk()
top.title("Deviation graph in Z (© F.Steven)")
top.geometry('550x150')
top.configure(bg= colour)



def reverse_colourmap(cmap, name = 'my_cmap_r'):
    reverse = []
    k = []

    for key in cmap._segmentdata:
        k.append(key)
        channel = cmap._segmentdata[key]
        data = []

        for t in channel:
            data.append((1-t[0],t[2],t[1]))
        reverse.append(sorted(data))

    LinearL = dict(zip(k,reverse))
    my_cmap_r = cm.colors.LinearSegmentedColormap(name, LinearL)
    return my_cmap_r



def grafico():
     cmap = cm.jet
     cmap_r = reverse_colourmap(cmap)

     filename = E1.get()
     if (exists(filename)):

          L3 = Label(top, text = "                                 ")
          L3.configure(bg = colour)
          L3.pack(padx = 5, pady = 5)
          L3.place(x = 190, y = 90)
          # print "no file input"
          quota_x =[]
          quota_y =[]
          angolo_x =[]
          angolo_y =[]
          count = 0

          lines = open(filename, "r").readlines()

          size = len(lines)
          for line in lines:
               if count > 175 and count < (size-1):
                    x = float(line[10:19])
                    y = float(line[21:31])
                    pitch = float(line[74:84])  #87:97
                    roll = float(line[61:71])
                    #errx = errx/4
                    quota_x.append(x)
                    quota_y.append(y)
                    angolo_x.append(pitch)
                    angolo_y.append(roll)
               count = count +1

          # Interpolazione dei dati
          x_new = np.linspace(min(quota_x), max(quota_x), 100)
          y_new = np.linspace(min(quota_y), max(quota_y), 100)
          x_new, y_new = np.meshgrid(x_new, y_new)

          # Interpolazione angolo_x e angolo_y
          angolo_x_interp = np.interp(x_new, quota_x, angolo_x)
          angolo_y_interp = np.interp(y_new, quota_y, angolo_y)

          # Calcolo delle coordinate z in base agli angoli interpolati
          z = np.sin(np.radians(angolo_x_interp)) + np.cos(np.radians(angolo_y_interp))

          # Creazione del grafico 3D
          fig = plt.figure()
          ax = fig.add_subplot(111, projection = '3d')

          # Grafico della superficie
          ax.plot_surface(x_new, y_new, z, cmap = 'viridis')

          # Aggiunta di etichette agli assi
          ax.set_xlabel('Quota X (mm)')
          ax.set_ylabel('Quota Y (mm)')
          ax.set_zlabel('Valore Z')

          # Visualizzazione del grafico
          plt.show()

     else:
          L3 = Label(top, text = "File non esiste", fg = "red")
          L3.pack(padx = 50, pady = 5)
          L3.place(x = 190, y = 90)

#scelta percorso da interfaccia
def select_file():
    filetypes = (('text files', '*.tab'),('All files', '*.*'))
    filename2 = fd.askopenfilename(title='Open a file',initialdir=r'C:\Users\sat11\Documents\GitHub\Parpas_DR\DroneXPairingSoftware - Sorgente\backend_app\src\states\output',filetypes=filetypes)
    E1.delete(0, "end")
    E1.insert(0,filename2)


#label
L1 = Label(top, text="Inserire percorso file di input:")
L1.pack( padx = 50, pady = 5)
L1.configure(bg= colour)
L1.place ( x = 10, y = 5)
#entry
E1 = Entry(top, bd =4)
E1.insert(0, r"C:\Users\sat11\Desktop\Dronex\SCANSIONI_MACCHINA_INCLINOMETRO\XXXXXXXXX____SCANSIONI_DroneX\XS167_scan\20231115_105316_XS167_XY_10000.0.tab")
E1.pack(padx = 50, pady = 5)
E1.place(x = 10, y = 35,width=530)

#bottone
b = tkinter.Button(top, text= "Visualizza\n grafico", bd =4, command = grafico)
b.pack(padx = 50, pady = 20)
b.place(x = 15, y = 80)


b2 = tkinter.Button(top, text= "Scegli percorso da PC", bd =4, command = select_file)
b2.pack(padx = 50, pady = 20)
b2.place(x =400, y = 80)



def quit():
    top.destroy()
    sys.exit()

#quit
top.protocol('WM_DELETE_WINDOW', quit)


#loop
top.mainloop()
