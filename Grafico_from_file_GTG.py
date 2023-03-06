

from mpl_toolkits.mplot3d import Axes3D
import matplotlib
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
import scipy.interpolate as interpolate
from scipy.interpolate import griddata
import matplotlib as mpl

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
          value =[]
          count = 0
          lines = open(filename, "r").readlines()

          size = len(lines)


          for line in lines:

              # dronex scan
              if count > 175 and count < (size-1):
                  words = line.split()
                  quota_x = float(words[1])
                  quota_y = float(words[2])
                  quota_z = float(words[3])
                  value_t = float(words[7])
                  x.append(quota_x)
                  y.append(quota_y)
                  z.append(quota_z)
                  value.append(value_t)


              '''#gtg scan 
              if count > 1 and count < (size):
                   words = line.split()
                   quota_x = float(words[2])
                   quota_y = float(words[3])
                   quota_z = float(words[4])
                   value_t = float(words[5])
                   x.append(quota_x)
                   y.append(quota_y)
                   z.append(quota_z)
                   value.append(value_t)'''

              count = count +1


          print(value)

          X = np.asarray(x)
          Y = np.asarray(y)
          Z = np.asarray(z)
          C = np.array(value)
          cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", [(0.94, 0, 0.05), (0.9, 0.81, 0.04),"lightgreen",
                                                                          (0.08, 0.78, 0.19), (0.9, 0.81, 0.04),
                                                                          (0.94, 0, 0.05)])

          fig = matplotlib.pyplot.gcf()
          xi = np.linspace(X.min(), X.max(), 100)
          yi = np.linspace(Y.min(), Y.max(), 100)
          zi = griddata((X, Y), Z, (xi[None, :], yi[:, None]), method = 'cubic')
          ci = griddata((X, Y), C, (xi[None, :], yi[:, None]), method = 'cubic')

          ax1 = fig.add_subplot(111, projection = '3d')
          xig, yig = np.meshgrid(xi, yi)
          norm = matplotlib.colors.Normalize(vmin = -0.005, vmax = 0.005)
          ax1.plot_surface(xig, yig, zi, facecolors = cmap(norm(ci)), cmap = cmap, vmin = -0.03, vmax = 0.03)
          ax1.figure.colorbar(mpl.cm.ScalarMappable(norm = norm, cmap = cmap), ax = ax1, pad = 0.12,shrink = 0.5, aspect = 15)
          plt.show()

          plt.show()
     else:
          L3 = Label(top, text = "File non esiste", fg = "red")
          L3.pack(padx = 50, pady = 5)
          L3.place(x = 190, y = 90)

#scelta percorso da interfaccia
def select_file():
    filetypes = (('text files', '*.tab'),('text files', '*.txt'),('All files', '*.*'))
    filename2 = fd.askopenfilename(title='Open a file',initialdir='/',filetypes=filetypes)
    E1.delete(0, "end")
    E1.insert(0,filename2)


#label
L1 = Label(top, text="Inserire percorso file di input:")
L1.pack( padx = 50, pady = 5)
L1.configure(bg= colour)
L1.place ( x = 10, y = 5)
#entry
E1 = Entry(top, bd =4)
E1.insert(0, r"C:/Users/sat11/Desktop/TRASFERTA_LOOKHEEDMARTIN/20230208_110746_DIA006_XY.tab")
#E1.insert(0, r"C:\Users\sat11\Desktop\Dronex\SCANSIONI_MACCHINA_INCLINOMETRO\XXXXXXXXX____SCANSIONI_DroneX\SPD014_scan\output_complex_20220201_142623.tab")
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
