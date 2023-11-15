

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
          x =[]
          y =[]
          z =[]
          count = 0
          lines = open(filename, "r").readlines()

          size = len(lines)
          for line in lines:
               if count > 175 and count < (size-1):
                    quota_x = float(line[10:19])
                    quota_y = float(line[21:31])
                    errx = float(line[98:108])  # err x  98:108   # angolo 61:71
                    errx= errx*1000
                    #if errx < 0:
                    #    errx = -errx
                    x.append(quota_x)
                    y.append(quota_y)
                    z.append(errx+1)

               count = count +1

          # Creazione di una griglia 2D per l'interpolazione
          grid_x, grid_y = np.mgrid[min(x):max(x):100j, min(y):max(y):100j]

          # Interpolazione dei dati
          grid_angle = griddata((x, y), z, (grid_x, grid_y), method = 'cubic')




          #normalized_data = (grid_angle - grid_angle.min()) / (grid_angle.max() - grid_angle.min())
          #grid_angle2 = np.log10(normalized_data)


          '''
          # Normalizza i dati
          normalized_data = (grid_angle - grid_angle.min()) / (grid_angle.max() - grid_angle.min()) # (0.05,0.05)#
          print(normalized_data)
          # Applica una trasformazione più marcata ai valori di Z
          grid_angle2 = np.power(normalized_data, 2)
          '''

          # Creazione del grafico 3D
          fig = plt.figure()
          ax = fig.add_subplot(111, projection = '3d')

          # Disegno della superficie interpolata
          surf = ax.plot_surface(grid_x, grid_y, grid_angle, cmap = cmap_r, edgecolor = 'k')
          fig.colorbar(surf, shrink = 0.5, aspect = 5)
          # Aggiunta di etichette
          ax.set_xlabel('Quota Asse X (mm)')
          ax.set_ylabel('Quota Asse Y (mm)')
          ax.set_zlabel('err (um)')  #Millesimi di grado

          # Mostra il grafico
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
